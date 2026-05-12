from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import require_api_key

router = APIRouter()


@router.get("/members", response_model=list[schemas.MemberOut])
def list_members(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    return db.query(models.Member).offset(offset).limit(page_size).all()


@router.get("/members/{id}", response_model=schemas.MemberOut)
def get_member(id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("/members", response_model=schemas.MemberOut, status_code=201)
def create_member(
    data: schemas.MemberCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    existing = db.query(models.Member).filter(models.Member.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    member = models.Member(**data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.patch("/members/{id}", response_model=schemas.MemberOut)
def update_member(
    id: int,
    data: schemas.MemberUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    member = db.query(models.Member).filter(models.Member.id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    db.commit()
    db.refresh(member)
    return member


@router.delete("/members/{id}", status_code=204)
def delete_member(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    member = db.query(models.Member).filter(models.Member.id == id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Check for active loans — cannot delete a member who has books out
    active_loans = db.query(models.Loan).filter(
        models.Loan.member_id == id,
        models.Loan.return_date == None
    ).first()
    if active_loans:
        raise HTTPException(status_code=409, detail="Cannot delete member with active loans")

    db.delete(member)
    db.commit()