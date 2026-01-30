from pydantic import BaseModel
from typing import Optional


class AnnotationCreate(BaseModel):
    username: str
    uri: str
    annotation: str
    openlibrary_work: Optional[int] = None
    openlibrary_edition: Optional[int] = None
    comment: Optional[str] = None
    private: bool = False


class AnnotationResponse(BaseModel):
    id: int
    username: str
    uri: str
    annotation: str
    openlibrary_work: Optional[int] = None
    openlibrary_edition: Optional[int] = None
    comment: Optional[str] = None
    private: bool

    class Config:
        from_attributes = True
