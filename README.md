# Moneytolia Link Shortener

This project is a URL shortening service developed using FastAPI. It works with an SQLite database and Redis cache.

## 🚀 Getting Started

### Requirements

- Docker
- Docker Compose

### Setup

1. Clone the project:
   ```bash
   git clone [project-url]
   cd [project-directory]
   ```

2. Start the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. The application will be running at `http://localhost:8000`.

### Environment Variables

Create a `.env` file and add the following variables:
```plaintext
REDIS_HOST=redis
REDIS_PORT=6379
```

## 📌 API Endpoints

#### Main Docs
```http
GET http://127.0.0.1:8000/docs
```
Main Docs

#### URL Shortening
```http
POST /shorten/
```
**Request Body:**
```json
{
    "target_url": "https://www.example.com"
}
```

**Successful Response:**
```json
{
    "original_url": "https://www.example.com",
    "short_code": "abc123",
    "clicks": 0
}
```

#### Redirection
```http
GET /{short_code}
```
Redirects the shortened URL to the original URL.

#### Statistics
```http
GET /url/{short_code}/stats
```
Returns statistics for the shortened URL.

#### Metrics Summary
```http
GET /url/metrics/summary
```
Returns metrics summary

#### Cache Cleaner
```http
POST /cache/clear/{short_code}
```
**Request Body:**
```json
{
}
```

## 🧪 Testing

To run tests:
```bash
docker-compose run test
```

