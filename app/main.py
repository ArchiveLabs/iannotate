from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from contextlib import asynccontextmanager
from app.database import get_db, init_db
from app.models import Annotation
from app.schemas import AnnotationCreate, AnnotationResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="iAnnotate API", version="1.0.0", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Internet Archive Annotations Server"}


@app.post("/annotations", response_model=AnnotationResponse)
def create_annotation(
    annotation: AnnotationCreate,
    db: Session = Depends(get_db)
):
    db_annotation = Annotation(**annotation.model_dump())
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation


@app.get("/annotations", response_model=List[AnnotationResponse])
def get_annotations(
    uri: Optional[str] = None,
    openlibrary_work: Optional[str] = None,
    openlibrary_edition: Optional[str] = None,
    username: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get annotations with optional filters.
    
    Query parameters:
    - uri: Filter by URI
    - openlibrary_work: Filter by OpenLibrary work ID
    - openlibrary_edition: Filter by OpenLibrary edition ID
    - username: Filter by username
    
    If no filters are provided, returns all annotations.
    """
    query = db.query(Annotation)
    
    if uri:
        query = query.filter(Annotation.uri == uri)
    if openlibrary_work:
        query = query.filter(Annotation.openlibrary_work == openlibrary_work)
    if openlibrary_edition:
        query = query.filter(Annotation.openlibrary_edition == openlibrary_edition)
    if username:
        query = query.filter(Annotation.username == username)
    
    annotations = query.all()
    return annotations
