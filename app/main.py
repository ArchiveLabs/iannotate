from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from enum import Enum
from contextlib import asynccontextmanager
from app.database import get_db, init_db
from app.models import Annotation
from app.schemas import AnnotationCreate, AnnotationResponse


class SortField(str, Enum):
    views = "views"
    created_date = "created_date"
    last_modified_date = "last_modified_date"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


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
    sort_by: Optional[SortField] = None,
    order: SortOrder = SortOrder.desc,
    db: Session = Depends(get_db)
):
    """
    Get annotations with optional filters and sorting.

    Query parameters:
    - uri / openlibrary_work / openlibrary_edition / username: filters
    - sort_by: views | created_date | last_modified_date
    - order: asc | desc (default desc)

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

    if sort_by:
        column = getattr(Annotation, sort_by.value)
        query = query.order_by(
            column.asc() if order == SortOrder.asc else column.desc()
        )

    annotations = query.all()
    return annotations


@app.put("/annotations", response_model=AnnotationResponse)
def update_views(
    annotation: str = Query(..., description="The snippet's annotation URL (unique key)"),
    views: Optional[int] = Query(
        None, description="Set views to this value; if omitted, increment by 1"
    ),
    db: Session = Depends(get_db),
):
    """Update a snippet's view count, keyed by its annotation URL."""
    obj = (
        db.query(Annotation)
        .filter(Annotation.annotation == annotation)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=404, detail="annotation not found")
    obj.views = views if views is not None else (obj.views or 0) + 1
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/annotations")
def delete_annotation(
    annotation: Optional[str] = Query(None, description="Delete by annotation URL"),
    id: Optional[int] = Query(None, description="Delete by id"),
    db: Session = Depends(get_db),
):
    """
    Delete a snippet (admin use). Not exposed through openlibrary.org — reachable
    only on the ol-home0 container, e.g. to remove spam.
    """
    if not annotation and id is None:
        raise HTTPException(status_code=400, detail="provide ?annotation= or ?id=")
    query = db.query(Annotation)
    query = (
        query.filter(Annotation.id == id)
        if id is not None
        else query.filter(Annotation.annotation == annotation)
    )
    obj = query.first()
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    deleted_id = obj.id
    db.delete(obj)
    db.commit()
    return {"deleted": True, "id": deleted_id}
