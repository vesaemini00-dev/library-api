from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import require_api_key

router = APIRouter()


@router.get("/authors", response_model=list[schemas.AuthorOut])
def list_authors(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    return db.query(models.Author).offset(offset).limit(page_size).all()


@router.get("/authors/{id}", response_model=schemas.AuthorOut)
def get_author(id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/authors", response_model=schemas.AuthorOut, status_code=201)
def create_author(
    data: schemas.AuthorCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    author = models.Author(**data.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.patch("/authors/{id}", response_model=schemas.AuthorOut)
def update_author(
    id: int,
    data: schemas.AuthorUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    author = db.query(models.Author).filter(models.Author.id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(author, field, value)
    db.commit()
    db.refresh(author)
    return author


@router.delete("/authors/{id}", status_code=204)
def delete_author(
    id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key)
):
    author = db.query(models.Author).filter(models.Author.id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()