from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app import models, schemas
from app.auth import require_api_key
import math

router = APIRouter()


@router.get("/books", response_model=list[schemas.BookOut])
def list_books(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    return (
        db.query(models.Book)
        .options(joinedload(models.Book.authors), joinedload(models.Book.category))
        .offset(offset)
        .limit(page_size)
        .all()
    )


@router.get("/books/search", response_model=schemas.PaginatedBooks)
def search_books(
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    author_id: Optional[int] = None,
    available_only: Optional[bool] = None,
    published_after: Optional[int] = None,
    published_before: Optional[int] = None,
    sort_by: Optional[str] = Query(default="title", enum=["title", "published_year", "popularity"]),
    sort_order: Optional[str] = Query(default="asc", enum=["asc", "desc"]),
    page: int = 1,
    page_size: int = Query(default=20, le=100),
    db: Session = Depends(get_db)
):
    query = (
        db.query(models.Book)
        .options(joinedload(models.Book.authors), joinedload(models.Book.category))
    )

    # Apply filters
    if q:
        query = query.filter(models.Book.title.ilike(f"%{q}%"))

    if category_id:
        query = query.filter(models.Book.category_id == category_id)

    if author_id:
        query = query.filter(models.Book.authors.any(models.Author.id == author_id))

    if published_after:
        query = query.filter(models.Book.published_year >= published_after)

    if published_before:
        query = query.filter(models.Book.published_year <= published_before)

    if available_only:
        active_loans = (
            db.query(func.count(models.Loan.id))
            .filter(
                models.Loan.book_id == models.Book.id,
                models.Loan.return_date == None
            )
            .correlate(models.Book)
            .scalar_subquery()
        )
        query = query.filter(models.Book.total_copies > active_loans)

    # Sorting
    if sort_by == "title":
        order_col = models.Book.title
    elif sort_by == "published_year":
        order_col = models.Book.published_year
    elif sort_by == "popularity":
        order_col = (
            db.query(func.count(models.Loan.id))
            .filter(models.Loan.book_id == models.Book.id)
            .correlate(models.Book)
            .scalar_subquery()
        )

    if sort_order == "desc":
        query = query.order_by(order_col.desc())
    else:
        query = query.order_by(order_col.asc())

    # Pagination
    total = query.count()
    total_pages = math.ceil(total / page_size)
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }


@router.get("/books/{id}", response_model=schemas.BookOut)
def get_book(id: int, db: Session = Depends(get_db)):
    book = (
        db.query(models.Book)
        .options(joinedload(models.Book.authors), joinedload(models.Book.category))
        .filter(models.Book.id == id)
        .first()
    )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/books", response_model=schemas.BookOut, status_code=201)
def create_book(
    data: schemas.BookCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    existing = db.query(models.Book).filter(models.Book.isbn == data.isbn).first()
    if existing:
        raise HTTPException(status_code=409, detail="ISBN already exists")

    category = db.query(models.Category).filter(models.Category.id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    book_data = data.model_dump(exclude={"author_ids"})
    book = models.Book(**book_data)

    if data.author_ids:
        authors = db.query(models.Author).filter(models.Author.id.in_(data.author_ids)).all()
        book.authors = authors

    db.add(book)
    db.commit()
    db.refresh(book)
    return get_book(book.id, db)


@router.patch("/books/{id}", response_model=schemas.BookOut)
def update_book(
    id: int,
    data: schemas.BookUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = data.model_dump(exclude_unset=True, exclude={"author_ids"})
    for field, value in update_data.items():
        setattr(book, field, value)

    if data.author_ids is not None:
        authors = db.query(models.Author).filter(models.Author.id.in_(data.author_ids)).all()
        book.authors = authors

    db.commit()
    db.refresh(book)
    return get_book(book.id, db)


@router.delete("/books/{id}", status_code=204)
def delete_book(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    active_loans = db.query(models.Loan).filter(
        models.Loan.book_id == id,
        models.Loan.return_date == None
    ).first()
    if active_loans:
        raise HTTPException(status_code=409, detail="Cannot delete book with active loans")

    db.delete(book)
    db.commit()


@router.get("/books/{id}/loan-history", response_model=schemas.PaginatedLoans)
def loan_history(
    id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    query = (
        db.query(models.Loan)
        .options(joinedload(models.Loan.member), joinedload(models.Loan.book))
        .filter(models.Loan.book_id == id)
        .order_by(models.Loan.loan_date.desc())
    )

    total = query.count()
    total_pages = math.ceil(total / page_size)
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }