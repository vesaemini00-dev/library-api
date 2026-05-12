from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional
from datetime import date
import math
from app.database import get_db
from app import models, schemas
from app.auth import require_api_key

router = APIRouter()


@router.post("/loans", response_model=schemas.LoanOut, status_code=201)
def borrow_book(
    data: schemas.LoanCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    # Check member exists
    member = db.query(models.Member).filter(models.Member.id == data.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Check member is active
    if not member.is_active:
        raise HTTPException(status_code=400, detail="Member is not active")

    # Check book exists
    book = db.query(models.Book).filter(models.Book.id == data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Count how many copies are currently on loan
    active_loans_count = db.query(func.count(models.Loan.id)).filter(
        models.Loan.book_id == data.book_id,
        models.Loan.return_date == None
    ).scalar()

    # Check if any copies are available
    if book.total_copies <= active_loans_count:
        raise HTTPException(status_code=409, detail="No copies available")

    # Create the loan
    loan = models.Loan(
        member_id=data.member_id,
        book_id=data.book_id,
        loan_date=date.today(),
        due_date=data.due_date,
        return_date=None
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)

    return (
        db.query(models.Loan)
        .options(
            joinedload(models.Loan.member),
            joinedload(models.Loan.book).joinedload(models.Book.authors),
            joinedload(models.Loan.book).joinedload(models.Book.category)
        )
        .filter(models.Loan.id == loan.id)
        .first()
    )


@router.post("/loans/{id}/return", response_model=schemas.LoanOut)
def return_book(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    loan = db.query(models.Loan).filter(models.Loan.id == id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    # Can't return a book that's already been returned
    if loan.return_date is not None:
        raise HTTPException(status_code=409, detail="Loan already returned")

    loan.return_date = date.today()
    db.commit()
    db.refresh(loan)

    return (
        db.query(models.Loan)
        .options(
            joinedload(models.Loan.member),
            joinedload(models.Loan.book).joinedload(models.Book.authors),
            joinedload(models.Loan.book).joinedload(models.Book.category)
        )
        .filter(models.Loan.id == id)
        .first()
    )


@router.get("/loans", response_model=schemas.PaginatedLoans)
def list_loans(
    member_id: Optional[int] = None,
    book_id: Optional[int] = None,
    status: Optional[str] = Query(default=None, enum=["active", "returned", "overdue"]),
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    query = (
        db.query(models.Loan)
        .options(
            joinedload(models.Loan.member),
            joinedload(models.Loan.book).joinedload(models.Book.authors),
            joinedload(models.Loan.book).joinedload(models.Book.category)
        )
    )

    # Filters
    if member_id:
        query = query.filter(models.Loan.member_id == member_id)

    if book_id:
        query = query.filter(models.Loan.book_id == book_id)

    if status == "active":
        query = query.filter(models.Loan.return_date == None)
    elif status == "returned":
        query = query.filter(models.Loan.return_date != None)
    elif status == "overdue":
        query = query.filter(
            models.Loan.return_date == None,
            models.Loan.due_date < date.today()
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