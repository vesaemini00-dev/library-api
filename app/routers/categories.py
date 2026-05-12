from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import require_api_key

router = APIRouter()


@router.get("/categories", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@router.get("/categories/{id}", response_model=schemas.CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    existing = db.query(models.Category).filter(models.Category.name == data.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Category name already exists")
    category = models.Category(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.patch("/categories/{id}", response_model=schemas.CategoryOut)
def update_category(
    id: int,
    data: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if data.name is not None:
        category.name = data.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{id}", status_code=204)
def delete_category(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()