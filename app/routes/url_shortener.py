from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import URL
from app.cache import URLCache
from app.metrics import CACHE_HITS, CACHE_MISSES, URL_RESPONSE_TIME
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import time

router = APIRouter()

class URLBase(BaseModel):
    target_url: HttpUrl

class URLInfo(BaseModel):
    original_url: str
    short_code: str
    clicks: int
    
    class Config:
        from_attributes = True  # orm_mode yerine from_attributes kullanıyoruz

@router.post("/shorten/", response_model=URLInfo)
async def create_short_url(url: URLBase, db: Session = Depends(get_db)):
    try:
        short_code = URL.generate_short_code()
        
        while db.query(URL).filter(URL.short_code == short_code).first():
            short_code = URL.generate_short_code()
        
        db_url = URL(
            original_url=str(url.target_url),
            short_code=short_code,
            clicks=0,
            is_active=True
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        
        return db_url
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{short_code}")
async def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL bulunamadı")
    
    db_url.clicks += 1
    db.commit()
    
    return RedirectResponse(url=db_url.original_url, status_code=302)

@router.get("/url/{short_code}/stats", response_model=URLInfo)
async def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL bulunamadı")
    return db_url

# Cache temizleme endpoint'i (opsiyonel)
@router.post("/cache/clear/{short_code}")
async def clear_url_cache(short_code: str):
    try:
        await URLCache.clear_cache(short_code)
        return {"message": "Cache temizlendi"}
    except Exception:
        raise HTTPException(status_code=500, detail="Cache temizlenemedi")

@router.get("/metrics/summary")
async def get_metrics_summary(db: Session = Depends(get_db)):
    total_urls = db.query(URL).count()
    active_urls = db.query(URL).filter(URL.is_active == True).count()
    total_clicks = db.query(URL).with_entities(func.sum(URL.clicks)).scalar() or 0
    
    return {
        "total_urls": total_urls,
        "active_urls": active_urls,
        "total_clicks": total_clicks,
        "status": "healthy"
    } 