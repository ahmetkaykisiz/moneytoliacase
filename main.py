from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import url_shortener
from app.database import engine
from app.models import Base

app = FastAPI(
    title="URL Kısaltma Servisi",
    description="FastAPI ile oluşturulmuş URL kısaltma servisi (SQLite)",
    version="1.0.0"
)

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ı ekle
app.include_router(url_shortener.router, tags=["url-shortener"])

@app.get("/")
async def root():
    return {"message": "URL Kısaltma Servisine Hoş Geldiniz!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Merhaba {name}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 