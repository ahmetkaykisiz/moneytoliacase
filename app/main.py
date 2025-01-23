from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from prometheus_fastapi_instrumentator import Instrumentator  # Bu satırı yoruma alın
from app.routes import url_shortener
from app.database import engine
from app.models import Base

app = FastAPI(
    title="Moneytolia Link Shortener Case",
    description="URL shortening service built with FastAPI (SQLite)",
    version="1.0.0"
)

# Bu satırı yoruma alın
# Instrumentator().instrument(app).expose(app)

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(url_shortener.router, tags=["url-shortener"])

@app.get("/")
async def root():
    return {
        "message": "Moneytolia Link Shortener Case",
        "kullanim": {
            "Shorten URL": "POST /shorten/ Shorten your URL.",
            "Statistics": "GET /url/{short_code}/stats and view the statistics.",
            "Redirection": "GET /{short_code} and navigate to the target URL."
        }
    } 