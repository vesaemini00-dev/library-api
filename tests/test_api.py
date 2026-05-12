from datetime import date, timedelta
from app import models


# ─── HEALTH CHECK ────────────────────────────────────────────────────

def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "library": "open"}


# ─── LOAN TESTS ──────────────────────────────────────────────────────

def test_borrow_book_success(client, sample_data, api_key_header):
    response = client.post("/api/v1/loans", json={
        "member_id": sample_data["member"].id,
        "book_id": sample_data["book"].id,
        "due_date": str(date.today() + timedelta(days=14))
    }, headers=api_key_header)
    assert response.status_code == 201
    data = response.json()
    assert data["member_id"] == sample_data["member"].id
    assert data["book_id"] == sample_data["book"].id
    assert data["return_date"] is None


def test_borrow_book_inactive_member(client, sample_data, api_key_header, db):
    sample_data["member"].is_active = False
    db.commit()

    response = client.post("/api/v1/loans", json={
        "member_id": sample_data["member"].id,
        "book_id": sample_data["book"].id,
        "due_date": str(date.today() + timedelta(days=14))
    }, headers=api_key_header)
    assert response.status_code == 400


def test_borrow_book_no_copies(client, sample_data, api_key_header, db):
    # Use all copies
    sample_data["book"].total_copies = 1
    db.commit()

    # First loan — should succeed
    client.post("/api/v1/loans", json={
        "member_id": sample_data["member"].id,
        "book_id": sample_data["book"].id,
        "due_date": str(date.today() + timedelta(days=14))
    }, headers=api_key_header)

    # Second loan — should fail with 409
    response = client.post("/api/v1/loans", json={
        "member_id": sample_data["member"].id,
        "book_id": sample_data["book"].id,
        "due_date": str(date.today() + timedelta(days=14))
    }, headers=api_key_header)
    assert response.status_code == 409


def test_return_book(client, sample_data, api_key_header):
    # First borrow
    borrow = client.post("/api/v1/loans", json={
        "member_id": sample_data["member"].id,
        "book_id": sample_data["book"].id,
        "due_date": str(date.today() + timedelta(days=14))
    }, headers=api_key_header)
    loan_id = borrow.json()["id"]

    # Then return
    response = client.post(f"/api/v1/loans/{loan_id}/return", headers=api_key_header)
    assert response.status_code == 200
    assert response.json()["return_date"] is not None


def test_return_already_returned(client, sample_data, api_key_header):
    # Borrow
    borrow = client.post("/api/v1/loans", json={
        "member_id": sample_data["member"].id,
        "book_id": sample_data["book"].id,
        "due_date": str(date.today() + timedelta(days=14))
    }, headers=api_key_header)
    loan_id = borrow.json()["id"]

    # Return once
    client.post(f"/api/v1/loans/{loan_id}/return", headers=api_key_header)

    # Return again — should fail
    response = client.post(f"/api/v1/loans/{loan_id}/return", headers=api_key_header)
    assert response.status_code == 409


# ─── SEARCH TESTS ────────────────────────────────────────────────────

def test_search_by_title(client, sample_data):
    response = client.get("/api/v1/books/search?q=1984")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "1984"


def test_search_no_results(client, sample_data):
    response = client.get("/api/v1/books/search?q=nonexistentbook")
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []


def test_search_by_category(client, sample_data):
    response = client.get(f"/api/v1/books/search?category_id={sample_data['category'].id}")
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_search_pagination_shape(client, sample_data):
    response = client.get("/api/v1/books/search?page=1&page_size=20")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "page" in data
    assert "page_size" in data
    assert "total" in data
    assert "total_pages" in data


def test_search_empty_page(client, sample_data):
    response = client.get("/api/v1/books/search?page=999")
    assert response.status_code == 200
    assert response.json()["items"] == []


# ─── AUTH TESTS ──────────────────────────────────────────────────────

def test_create_without_api_key(client, sample_data):
    response = client.post("/api/v1/categories", json={"name": "Test"})
    assert response.status_code == 422


def test_create_with_wrong_api_key(client, sample_data):
    response = client.post(
        "/api/v1/categories",
        json={"name": "Test"},
        headers={"X-API-Key": "wrongkey"}
    )
    assert response.status_code == 401