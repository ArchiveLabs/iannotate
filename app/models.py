from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    uri = Column(String, nullable=False, index=True)
    annotation = Column(String, nullable=False)
    openlibrary_work = Column(String, nullable=True, index=True)
    openlibrary_edition = Column(String, nullable=True, index=True)
    comment = Column(String, nullable=True)
    private = Column(Boolean, nullable=False, default=False)
    views = Column(Integer, nullable=False, default=0, server_default="0")
    created_date = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    last_modified_date = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
