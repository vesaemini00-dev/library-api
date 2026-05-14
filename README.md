cat > README.md << 'ENDOFFILE'
# Library API

A RESTful backend API for a small library lending system, built with FastAPI and SQLAlchemy. The API allows librarians to manage books, authors, categories, and members, and to track book loans.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **SQLite** — database (development)
- **pytest** — testing

---

## Setup Instructions

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/vesaemini00-dev/library-api.git
cd library-api
\`\`\`

### 2. Create and activate virtual environment

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Set environment variables

Create a \`.env\` file in the root folder:

\`\`\`
DATABASE_URL=sqlite:///./library.db
API_KEY=mysecretapikey123
\`\`\`

### 5. Apply database migrations

\`\`\`bash
alembic upgrade head
\`\`\`

### 6. Seed the database

\`\`\`bash
python3 scripts/seed.py
\`\`\`

### 7. Run the server

\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

API available at: http://127.0.0.1:8000
Interactive docs: http://127.0.0.1:8000/docs

---

## Run with Docker

\`\`\`bash
docker compose up
\`\`\`

---

## Run Tests

\`\`\`bash
PYTHONPATH=. pytest tests/ -v
\`\`\`

---

## API Key

All POST, PATCH, and DELETE endpoints require this header:

\`\`\`
X-API-Key: mysecretapikey123
\`\`\`

---

## Endpoints

- GET /api/v1/health — health check
- GET/POST/PATCH/DELETE /api/v1/books — book management
- GET /api/v1/books/search — search with filters, sorting, pagination
- GET /api/v1/books/{id}/loan-history — loan history for a book
- GET/POST/PATCH/DELETE /api/v1/members — member management
- GET/POST/PATCH/DELETE /api/v1/authors — author management
- GET/POST/PATCH/DELETE /api/v1/categories — category management
- POST /api/v1/loans — borrow a book
- POST /api/v1/loans/{id}/return — return a book
- GET /api/v1/loans — list loans with filters
- GET /api/v1/reports/top-borrowers — top borrowing members
- GET /api/v1/reports/overdue-loans — all overdue loans

---

## Notes
lighthouse

## Limitations
- SQLite is used for development — switch DATABASE_URL to PostgreSQL for production
- No rate limiting on endpoints
- API key auth is simple — a production system would use JWT tokens
ENDOFFILE