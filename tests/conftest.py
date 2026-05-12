import os
os.environ["API_KEY"] = "secret"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app import models
from datetime import date

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    database = TestingSessionLocal()
    yield database
    database.close()


@pytest.fixture
def api_key_header():
    return {"X-API-Key": "secret"}


@pytest.fixture
def sample_data(db):
    category = models.Category(name="Fiction")
    db.add(category)
    db.commit()

    author = models.Author(full_name="George Orwell", country="UK")
    db.add(author)
    db.commit()

    book = models.Book(
        title="1984",
        isbn="978-0451524935",
        published_year=1949,
        total_copies=3,
        category_id=category.id
    )
    book.authors = [author]
    db.add(book)
    db.commit()

    member = models.Member(
        full_name="Alice Johnson",
        email="alice@test.com",
        join_date=date(2023, 1, 1),
        is_active=True
    )
    db.add(member)
    db.commit()

    return {
        "category": category,
        "author": author,
        "book": book,
        "member": member
    }