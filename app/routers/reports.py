from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/reports/top-borrowers", response_model=list[schemas.TopBorrower])
def top_borrowers(
    limit: int = Query(default=5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            models.Member.id,
            models.Member.full_name,
            models.Member.email,
            func.count(models.Loan.id).label("total_loans")
        )
        .join(models.Loan, models.Loan.member_id == models.Member.id)
        .group_by(models.Member.id)
        .order_by(func.count(models.Loan.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": r.id,
            "full_name": r.full_name,
            "email": r.email,
            "total_loans": r.total_loans
        }
        for r in results
    ]


@router.get("/reports/overdue-loans", response_model=list[schemas.OverdueLoan])
def overdue_loans(db: Session = Depends(get_db)):
    today = date.today()

    results = (
        db.query(
            models.Loan.id.label("loan_id"),
            models.Member.full_name.label("member_name"),
            models.Book.title.label("book_title"),
            models.Loan.due_date,
            (today - models.Loan.due_date).label("days_overdue")
        )
        .join(models.Member, models.Loan.member_id == models.Member.id)
        .join(models.Book, models.Loan.book_id == models.Book.id)
        .filter(
            models.Loan.return_date == None,
            models.Loan.due_date < today
        )
        .all()
    )

    return [
        {
            "loan_id": r.loan_id,
            "member_name": r.member_name,
            "book_title": r.book_title,
            "due_date": r.due_date,
            "days_overdue": (today - r.due_date).days
        }
        for r in results
    ]