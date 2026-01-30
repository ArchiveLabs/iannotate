# iannotate
Internet Archive (W3C) Annotations Server

A minimal Python, FastAPI, Postgres, SQLAlchemy application for managing annotations.

## Features

- **Database Table**: `annotations` with the following columns:
  - `username`: Username of the annotator
  - `uri`: e.g., "https://archive.org/details/itemname{/subfile}" (defines the item being annotated)
  - `annotation`: URL of the annotation
  - `openlibrary_work`: Optional OpenLibrary work ID (integer)
  - `openlibrary_edition`: Optional OpenLibrary edition ID (integer)
  - `comment`: Optional comment (string)
  - `private`: Boolean indicating if the annotation is private

## API Endpoints

- `POST /annotations`: Create a new annotation
- `GET /annotations`: Fetch all annotations
- `GET /annotations/by-uri`: Fetch annotations by itemname and optional subfile
- `GET /annotations/by-work/{work_id}`: Fetch annotations by OpenLibrary work ID
- `GET /annotations/by-edition/{edition_id}`: Fetch annotations by OpenLibrary edition ID

## Quick Start

### Using Docker Compose (Recommended)

1. Start the application:
```bash
docker-compose up --build
```

2. The API will be available at http://localhost:8000

3. View API documentation at http://localhost:8000/docs

### Example API Usage

Create an annotation:
```bash
curl -X POST "http://localhost:8000/annotations" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "uri": "https://archive.org/details/item123",
    "annotation": "http://example.com/annotation/1",
    "openlibrary_work": 12345,
    "comment": "Interesting book",
    "private": false
  }'
```

Fetch annotations by URI:
```bash
curl "http://localhost:8000/annotations/by-uri?itemname=item123"
```

Fetch annotations by OpenLibrary work ID:
```bash
curl "http://localhost:8000/annotations/by-work/12345"
```

## Development

### Requirements

- Docker and Docker Compose
- Python 3.11+ (for local development)

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
