from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    uri = Column(String, nullable=False, index=True)
    annotation = Column(String, nullable=False)
    openlibrary_work = Column(Integer, nullable=True, index=True)
    openlibrary_edition = Column(Integer, nullable=True, index=True)
    comment = Column(String, nullable=True)
    private = Column(Boolean, nullable=False, default=False)
