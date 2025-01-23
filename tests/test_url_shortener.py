import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Ana sayfa testi"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_url():
    """URL kısaltma testi"""
    response = client.post(
        "/shorten/",
        json={"target_url": "https://www.example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert "original_url" in data

def test_invalid_url():
    """Geçersiz URL testi"""
    response = client.post(
        "/shorten/",
        json={"target_url": "invalid-url"}
    )
    assert response.status_code == 422

def test_url_flow():
    """URL akışı testi (oluşturma, yönlendirme ve istatistikler)"""
    # 1. URL oluştur
    create_response = client.post(
        "/shorten/",
        json={"target_url": "https://www.example.com"}
    )
    assert create_response.status_code == 200
    short_code = create_response.json()["short_code"]

    # 2. URL'ye eriş
    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code in [302, 307]

    # 3. İstatistikleri kontrol et
    stats_response = client.get(f"/url/{short_code}/stats")
    assert stats_response.status_code == 200

def test_metrics():
    """Metrik özeti testi"""
    response = client.get("/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_urls" in data
    assert "total_clicks" in data