import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop them after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Internet Archive Annotations Server"}


def test_create_annotation():
    """Test creating a new annotation (CREATE)"""
    annotation_data = {
        "username": "alice",
        "uri": "https://archive.org/details/item123",
        "annotation": "http://example.com/annotation/1",
        "openlibrary_work": "OL12345W",
        "openlibrary_edition": "OL67890M",
        "comment": "Interesting book",
        "private": False
    }
    response = client.post("/annotations", json=annotation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["uri"] == "https://archive.org/details/item123"
    assert data["annotation"] == "http://example.com/annotation/1"
    assert data["openlibrary_work"] == "OL12345W"
    assert data["openlibrary_edition"] == "OL67890M"
    assert data["comment"] == "Interesting book"
    assert data["private"] is False
    assert "id" in data


def test_get_all_annotations():
    """Test retrieving all annotations (READ)"""
    # Create test annotations
    annotation1 = {
        "username": "alice",
        "uri": "https://archive.org/details/item1",
        "annotation": "http://example.com/annotation/1",
        "private": False
    }
    annotation2 = {
        "username": "bob",
        "uri": "https://archive.org/details/item2",
        "annotation": "http://example.com/annotation/2",
        "private": True
    }
    client.post("/annotations", json=annotation1)
    client.post("/annotations", json=annotation2)
    
    # Get all annotations
    response = client.get("/annotations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "alice"
    assert data[1]["username"] == "bob"


def test_get_annotations_by_uri():
    """Test filtering annotations by URI"""
    # Create test annotations with different URIs
    annotation1 = {
        "username": "alice",
        "uri": "https://archive.org/details/item123",
        "annotation": "http://example.com/annotation/1",
        "private": False
    }
    annotation2 = {
        "username": "bob",
        "uri": "https://archive.org/details/item123",
        "annotation": "http://example.com/annotation/2",
        "private": False
    }
    annotation3 = {
        "username": "charlie",
        "uri": "https://archive.org/details/item456",
        "annotation": "http://example.com/annotation/3",
        "private": False
    }
    client.post("/annotations", json=annotation1)
    client.post("/annotations", json=annotation2)
    client.post("/annotations", json=annotation3)
    
    # Filter by URI
    response = client.get("/annotations?uri=https://archive.org/details/item123")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(ann["uri"] == "https://archive.org/details/item123" for ann in data)


def test_get_annotations_by_openlibrary_work():
    """Test filtering annotations by OpenLibrary work ID"""
    # Create test annotations with different work IDs
    annotation1 = {
        "username": "alice",
        "uri": "https://archive.org/details/item1",
        "annotation": "http://example.com/annotation/1",
        "openlibrary_work": "OL12345W",
        "private": False
    }
    annotation2 = {
        "username": "bob",
        "uri": "https://archive.org/details/item2",
        "annotation": "http://example.com/annotation/2",
        "openlibrary_work": "OL12345W",
        "private": False
    }
    annotation3 = {
        "username": "charlie",
        "uri": "https://archive.org/details/item3",
        "annotation": "http://example.com/annotation/3",
        "openlibrary_work": "OL99999W",
        "private": False
    }
    client.post("/annotations", json=annotation1)
    client.post("/annotations", json=annotation2)
    client.post("/annotations", json=annotation3)
    
    # Filter by work ID
    response = client.get("/annotations?openlibrary_work=OL12345W")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(ann["openlibrary_work"] == "OL12345W" for ann in data)


def test_get_annotations_by_openlibrary_edition():
    """Test filtering annotations by OpenLibrary edition ID"""
    # Create test annotations with different edition IDs
    annotation1 = {
        "username": "alice",
        "uri": "https://archive.org/details/item1",
        "annotation": "http://example.com/annotation/1",
        "openlibrary_edition": "OL67890M",
        "private": False
    }
    annotation2 = {
        "username": "bob",
        "uri": "https://archive.org/details/item2",
        "annotation": "http://example.com/annotation/2",
        "openlibrary_edition": "OL11111M",
        "private": False
    }
    client.post("/annotations", json=annotation1)
    client.post("/annotations", json=annotation2)
    
    # Filter by edition ID
    response = client.get("/annotations?openlibrary_edition=OL67890M")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["openlibrary_edition"] == "OL67890M"


def test_get_annotations_by_username():
    """Test filtering annotations by username"""
    # Create test annotations with different usernames
    annotation1 = {
        "username": "alice",
        "uri": "https://archive.org/details/item1",
        "annotation": "http://example.com/annotation/1",
        "private": False
    }
    annotation2 = {
        "username": "alice",
        "uri": "https://archive.org/details/item2",
        "annotation": "http://example.com/annotation/2",
        "private": False
    }
    annotation3 = {
        "username": "bob",
        "uri": "https://archive.org/details/item3",
        "annotation": "http://example.com/annotation/3",
        "private": False
    }
    client.post("/annotations", json=annotation1)
    client.post("/annotations", json=annotation2)
    client.post("/annotations", json=annotation3)
    
    # Filter by username
    response = client.get("/annotations?username=alice")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(ann["username"] == "alice" for ann in data)


def test_get_annotations_with_multiple_filters():
    """Test filtering annotations with multiple query parameters"""
    # Create test annotations
    annotation1 = {
        "username": "alice",
        "uri": "https://archive.org/details/item123",
        "annotation": "http://example.com/annotation/1",
        "openlibrary_work": "OL12345W",
        "private": False
    }
    annotation2 = {
        "username": "alice",
        "uri": "https://archive.org/details/item456",
        "annotation": "http://example.com/annotation/2",
        "openlibrary_work": "OL12345W",
        "private": False
    }
    annotation3 = {
        "username": "bob",
        "uri": "https://archive.org/details/item123",
        "annotation": "http://example.com/annotation/3",
        "openlibrary_work": "OL12345W",
        "private": False
    }
    client.post("/annotations", json=annotation1)
    client.post("/annotations", json=annotation2)
    client.post("/annotations", json=annotation3)
    
    # Filter by multiple parameters
    response = client.get("/annotations?username=alice&openlibrary_work=OL12345W")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(ann["username"] == "alice" and ann["openlibrary_work"] == "OL12345W" for ann in data)


def test_create_annotation_minimal_fields():
    """Test creating annotation with only required fields"""
    annotation_data = {
        "username": "minimaluser",
        "uri": "https://archive.org/details/minimal",
        "annotation": "http://example.com/annotation/minimal"
    }
    response = client.post("/annotations", json=annotation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "minimaluser"
    assert data["openlibrary_work"] is None
    assert data["openlibrary_edition"] is None
    assert data["comment"] is None
    assert data["private"] is False


def test_empty_result_set():
    """Test that querying with no matching results returns empty list"""
    response = client.get("/annotations?username=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data == []
