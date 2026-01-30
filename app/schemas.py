from pydantic import BaseModel
from typing import Optional


class AnnotationCreate(BaseModel):
    username: str
    uri: str
    annotation: str
    openlibrary_work: Optional[str] = None
    openlibrary_edition: Optional[str] = None
    comment: Optional[str] = None
    private: bool = False


class AnnotationResponse(BaseModel):
    id: int
    username: str
    uri: str
    annotation: str
    openlibrary_work: Optional[str] = None
    openlibrary_edition: Optional[str] = None
    comment: Optional[str] = None
    private: bool

    class Config:
        from_attributes = True
