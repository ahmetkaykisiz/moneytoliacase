from prometheus_client import Counter, Histogram, Gauge
import time

# URL Metrikleri
URL_REQUESTS_TOTAL = Counter(
    'url_shortener_requests_total',
    'Toplam URL kısaltma istekleri',
    ['method', 'endpoint']
)

URL_RESPONSE_TIME = Histogram(
    'url_shortener_response_time_seconds',
    'Endpoint yanıt süreleri',
    ['method', 'endpoint']
)

ACTIVE_URLS = Gauge(
    'url_shortener_active_urls',
    'Aktif kısa URL sayısı'
)

CACHE_HITS = Counter(
    'url_shortener_cache_hits_total',
    'Cache isabet sayısı'
)

CACHE_MISSES = Counter(
    'url_shortener_cache_misses_total',
    'Cache kaçırma sayısı'
)

# Performans Metrikleri
REDIS_RESPONSE_TIME = Histogram(
    'url_shortener_redis_response_time_seconds',
    'Redis yanıt süreleri'
)

DB_RESPONSE_TIME = Histogram(
    'url_shortener_db_response_time_seconds',
    'Veritabanı yanıt süreleri'
) 