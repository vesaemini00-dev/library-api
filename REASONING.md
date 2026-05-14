# Reasoning & Design Decisions

## Why I chose SQLite
I went with SQLite for this project because it was the simplest option for development. It doesn't need a separate server running, it just saves everything into a file called library.db. Since the assessment didn't require a production deployment, SQLite made sense. If I were to take this to production I would switch to PostgreSQL by just updating the DATABASE_URL environment variable.

## Why I modelled the M:N relationship the way I did
A book can have multiple authors and an author can have multiple books. This is a many to many relationship. I created a separate table called book_authors that holds two columns — book_id and author_id — together forming the primary key. This is the standard way to handle M:N in relational databases. In SQLAlchemy I used the secondary parameter in the relationship() call so I can just write book.authors and get the list of authors back without manually writing JOIN queries every time.

## How I avoided N+1 queries in the search endpoint
The N+1 problem happens when you fetch a list of items and then make a separate database query for each item to get its related data. In my case, if I fetched 20 books and then loaded each book's authors separately, that would be 21 queries total. I avoided this by using joinedload() from SQLAlchemy, which tells the ORM to fetch the books and their authors together in one JOIN query. This means no matter how many books are returned, it's always one query.

## Why DELETE on a member with active loans returns 409
If a member still has books out and we delete them, the loan records in the database would be left pointing to a member that no longer exists. This breaks the data. A 409 Conflict is the correct HTTP status here because the request itself is valid — we just can't complete it in the current state. The caller needs to make sure all books are returned first before the member can be deleted.

## How I structured my test suite
I used pytest with a separate test database so tests never touch the real data. I set up a conftest.py file with shared fixtures — a test client, a database session, sample data, and an API key header — so I don't repeat setup code in every test. I focused on testing the loan endpoints because they have the most business logic (checking if a member is active, checking available copies, handling returns). I also tested the search endpoint to make sure filters and pagination work correctly. I skipped testing basic CRUD endpoints individually because the pattern is the same across all resources and the loan tests already cover the core behaviours.

## Scope choices
Everything required in the brief was completed:
- All CRUD endpoints for books, members, authors, and categories
- Loan endpoints with all the required business logic
- Book search with filters, sorting, and pagination
- Reports (top borrowers and overdue loans)
- API key authentication on all write endpoints
- Alembic migrations
- Seed script with 20 books, 10 authors, 10 members, and 31 loans
- pytest tests
- Docker setup

Nothing was cut.

## External resources used
- FastAPI documentation: https://fastapi.tiangolo.com
- SQLAlchemy documentation: https://docs.sqlalchemy.org
- Alembic documentation: https://alembic.sqlalchemy.org
- Giga Academy Batch 5 course material
- Claude AI (Anthropic) — used with the following prompts:
  - "what is an ORM and why do we use it instead of raw SQL"
  - "how do I set up Alembic migrations with SQLAlchemy"
  - "what is the N+1 problem and how do I avoid it"
  - "how does joinedload work and when should I use it"
  - "how do I create a many to many relationship in SQLAlchemy"
  - "why does PATCH use exclude_unset=True"
  - "how do I protect FastAPI endpoints with an API key header"
  - "what is the difference between 400 and 409 HTTP status codes"
  - "how do I write pytest fixtures and what is conftest.py"
  - "how do I use subqueries in SQLAlchemy to count related records"
