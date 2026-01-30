from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db, init_db
from app.models import Annotation
from app.schemas import AnnotationCreate, AnnotationResponse
import re

app = FastAPI(title="iAnnotate API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    init_db()


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
def get_all_annotations(db: Session = Depends(get_db)):
    annotations = db.query(Annotation).all()
    return annotations


@app.get("/annotations/by-uri", response_model=List[AnnotationResponse])
def get_annotations_by_uri(
    itemname: str,
    subfile: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if subfile:
        uri = f"https://archive.org/details/{itemname}/{subfile}"
    else:
        uri = f"https://archive.org/details/{itemname}"
    
    annotations = db.query(Annotation).filter(Annotation.uri == uri).all()
    return annotations


@app.get("/annotations/by-work/{work_id}", response_model=List[AnnotationResponse])
def get_annotations_by_work(
    work_id: int,
    db: Session = Depends(get_db)
):
    annotations = db.query(Annotation).filter(
        Annotation.openlibrary_work == work_id
    ).all()
    return annotations


@app.get("/annotations/by-edition/{edition_id}", response_model=List[AnnotationResponse])
def get_annotations_by_edition(
    edition_id: int,
    db: Session = Depends(get_db)
):
    annotations = db.query(Annotation).filter(
        Annotation.openlibrary_edition == edition_id
    ).all()
    return annotations
