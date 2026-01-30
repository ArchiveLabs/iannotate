# iannotate
Internet Archive (W3C) Annotations Server

A minimal Python, FastAPI, Postgres, SQLAlchemy application for managing annotations.

## Purpose

This service provides a RESTful API for storing and retrieving annotations associated with Internet Archive items and OpenLibrary works/editions. It supports filtering annotations by URI, OpenLibrary work/edition IDs, and username.

## Quick Start

### Using Docker Compose (Recommended)

1. Start the application:
```bash
docker-compose up --build
```

2. The API will be available at http://localhost:8000

3. View API documentation at http://localhost:8000/docs

## API Endpoints

### Create Annotation
- `POST /annotations`: Create a new annotation

### Get Annotations
- `GET /annotations`: Fetch all annotations or filter using query parameters:
  - `?uri={uri}`: Filter by URI
  - `?openlibrary_work={work_id}`: Filter by OpenLibrary work ID
  - `?openlibrary_edition={edition_id}`: Filter by OpenLibrary edition ID
  - `?username={username}`: Filter by username
  
Query parameters can be combined to filter by multiple criteria.

### Example Usage

Create an annotation:
```bash
curl -X POST "http://localhost:8000/annotations" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "uri": "https://archive.org/details/item123",
    "annotation": "http://example.com/annotation/1",
    "openlibrary_work": "OL12345W",
    "comment": "Interesting book",
    "private": false
  }'
```

Fetch all annotations:
```bash
curl "http://localhost:8000/annotations"
```

Fetch annotations by URI:
```bash
curl "http://localhost:8000/annotations?uri=https://archive.org/details/item123"
```

Fetch annotations by OpenLibrary work ID:
```bash
curl "http://localhost:8000/annotations?openlibrary_work=OL12345W"
```

Fetch annotations by username:
```bash
curl "http://localhost:8000/annotations?username=alice"
```

Fetch with multiple filters:
```bash
curl "http://localhost:8000/annotations?username=alice&openlibrary_work=OL12345W"
```

## Running Tests

Install test dependencies:
```bash
pip install -r requirements.txt
```

Run the test suite:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

## Development

### Requirements

- Docker and Docker Compose (recommended)
- Python 3.11+ (for local development)
- PostgreSQL (for local development without Docker)

### Local Development Without Docker

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up a PostgreSQL database and configure the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/iannotate
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```
