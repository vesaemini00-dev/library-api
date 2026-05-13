# Reasoning & Design Decisions

## Notes
lighthouse

## Project Overview
A RESTful library lending API built with FastAPI, SQLAlchemy, and Alembic. The API manages books, authors, categories, members, and loans.

## Endpoints
See README.md for the full list of endpoints, or visit /docs for the interactive Swagger UI.

---

## Design Decisions

### Why SQLite?
SQLite was chosen for development because it requires zero configuration — it's just a file on disk. This makes it easy to clone and run the project without setting up a separate database server. The app can be switched to PostgreSQL by changing the DATABASE_URL environment variable.

### How I modelled the M:N relationship (books and authors)
A book can have multiple authors, and an author can have multiple books. This is a many-to-many relationship. I implemented it using an association table called `book_authors` with two columns: `book_id` and `author_id`, forming a composite primary key. SQLAlchemy handles this with the `secondary` parameter in the `relationship()` call, so you can do `book.authors` and get a list of author objects directly.

### How I avoided N+1 queries in the search endpoint
Without eager loading, fetching 20 books would trigger 20 additional queries to load each book's authors — one per book. This is called the N+1 problem. I solved it using SQLAlchemy's `joinedload()`, which tells the ORM to fetch books and their authors in a single JOIN query. This means the search endpoint always uses one query for items regardless of how many results are returned.

### Why DELETE on a member with active loans returns 409
A 409 Conflict means the request is valid but cannot be completed because of the current state of the resource. Deleting a member who still has books out would leave orphaned loan records in the database — loans with no member attached. This would corrupt the data. Returning 409 tells the caller they need to resolve the conflict first (return the books) before the delete can proceed.

### How I structured the test suite
I used pytest with a separate in-memory SQLite test database so tests never touch production data. A `conftest.py` file sets up fixtures shared across all tests: a test client, a database session, sample data, and an API key header. I focused tests on the loan endpoints (the core business logic) and the search endpoint (filters, pagination shape). I skipped testing every CRUD endpoint individually as the pattern is repetitive and the loan/search tests cover the most meaningful behaviour.

### How authentication works
All POST, PATCH, and DELETE endpoints are protected with a simple API key check. FastAPI reads the `X-API-Key` header from the request and compares it against the `API_KEY` environment variable. If the key is missing or wrong, a 401 Unauthorized is returned. GET endpoints are open because they only read data.

---

## Scope Choices
- All required endpoints implemented
- Seed data meets minimum requirements (20 books, 10 authors, 10 members, 31 loans)
- Docker and Alembic migrations included
- Tests cover loan flow and search endpoint

## Limitations & Known Issues
- SQLite does not support all PostgreSQL features; date arithmetic in the overdue report uses Python instead of pure SQL for compatibility
- No rate limiting on endpoints
- API key authentication is simple; a production system would use JWT tokens

---

## External Resources Used
- FastAPI documentation: https://fastapi.tiangolo.com
- SQLAlchemy documentation: https://docs.sqlalchemy.org
- Alembic documentation: https://alembic.sqlalchemy.org
- Claude AI (Anthropic) — used to unblock syntax questions and understand concepts during development