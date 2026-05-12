from fastapi import FastAPI
from app.routers import books, members, authors, categories, loans, reports

app = FastAPI(
    title="Library API",
    description="A library lending system API",
    version="1.0.0"
)

# Register all routers
app.include_router(books.router, prefix="/api/v1", tags=["Books"])
app.include_router(members.router, prefix="/api/v1", tags=["Members"])
app.include_router(authors.router, prefix="/api/v1", tags=["Authors"])
app.include_router(categories.router, prefix="/api/v1", tags=["Categories"])
app.include_router(loans.router, prefix="/api/v1", tags=["Loans"])
app.include_router(reports.router, prefix="/api/v1", tags=["Reports"])


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "library": "open"}