from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


# ─── CATEGORY ────────────────────────────────────────────────────────

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int

    model_config = {"from_attributes": True}


# ─── AUTHOR ──────────────────────────────────────────────────────────

class AuthorBase(BaseModel):
    full_name: str
    country: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    full_name: Optional[str] = None
    country: Optional[str] = None

class AuthorOut(AuthorBase):
    id: int

    model_config = {"from_attributes": True}


# ─── BOOK ────────────────────────────────────────────────────────────

class BookBase(BaseModel):
    title: str
    isbn: str
    published_year: Optional[int] = None
    total_copies: int = 1
    category_id: int

class BookCreate(BookBase):
    author_ids: List[int] = []

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: Optional[int] = None
    category_id: Optional[int] = None
    author_ids: Optional[List[int]] = None

class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    published_year: Optional[int]
    total_copies: int
    category: CategoryOut
    authors: List[AuthorOut] = []

    model_config = {"from_attributes": True}


# ─── MEMBER ──────────────────────────────────────────────────────────

class MemberBase(BaseModel):
    full_name: str
    email: str
    join_date: date
    is_active: bool = True

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class MemberOut(MemberBase):
    id: int

    model_config = {"from_attributes": True}


# ─── LOAN ────────────────────────────────────────────────────────────

class LoanCreate(BaseModel):
    member_id: int
    book_id: int
    due_date: date

class LoanOut(BaseModel):
    id: int
    member_id: int
    book_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date] = None
    member: MemberOut
    book: BookOut

    model_config = {"from_attributes": True}


# ─── PAGINATION ──────────────────────────────────────────────────────

class PaginatedBooks(BaseModel):
    items: List[BookOut]
    page: int
    page_size: int
    total: int
    total_pages: int

class PaginatedLoans(BaseModel):
    items: List[LoanOut]
    page: int
    page_size: int
    total: int
    total_pages: int


# ─── REPORTS ─────────────────────────────────────────────────────────

class TopBorrower(BaseModel):
    id: int
    full_name: str
    email: str
    total_loans: int

    model_config = {"from_attributes": True}

class OverdueLoan(BaseModel):
    loan_id: int
    member_name: str
    book_title: str
    due_date: date
    days_overdue: int

    model_config = {"from_attributes": True}


# ─── ERROR ───────────────────────────────────────────────────────────

class ErrorOut(BaseModel):
    detail: str