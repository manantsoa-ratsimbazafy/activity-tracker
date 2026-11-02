from dotenv import load_dotenv
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.db import Base, get_db
from app.models import Activity, TimeEntry


load_dotenv()
db_url = os.getenv("DATABASE_URL")
db_test_url = os.getenv("TEST_DATABASE_URL")

if not db_test_url:
    raise RuntimeError("TEST_DATABASE_URL is missing in the .env file")

if db_test_url == db_url:
    raise RuntimeError("The test database url can't be the same as the main database")

engine = create_engine(db_test_url)

SessionTest = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

def get_test_db():
    
    test_db = SessionTest()
    
    try:
        yield test_db
    finally:
        test_db.close()

@pytest.fixture
def create_test_tables():
    
    Base.metadata.create_all(engine)
    
    yield

    Base.metadata.drop_all(engine)
    
@pytest.fixture
def client(create_test_tables):
    
    app.dependency_overrides[get_db] = get_test_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()
    
@pytest.fixture
def created_activity(client):
    
    create_response = client.post("/activities", json={"name": "test"})
    
    return create_response.json()["id"]