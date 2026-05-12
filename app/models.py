from sqlalchemy import (
    Column, Integer, String, Boolean, Date, 
    ForeignKey, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from app.database import Base


# ─── ASSOCIATION TABLE ───────────────────────────────────────────────
class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)


# ─── CATEGORY ────────────────────────────────────────────────────────
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # One category has many books
    books = relationship("Book", back_populates="category")


# ─── AUTHOR ──────────────────────────────────────────────────────────
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    country = Column(String, nullable=True)

    # Many authors <-> many books (through book_authors table)
    books = relationship("Book", secondary="book_authors", back_populates="authors")


# ─── BOOK ────────────────────────────────────────────────────────────
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    published_year = Column(Integer, nullable=True)
    total_copies = Column(Integer, nullable=False, default=1)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint("total_copies >= 0", name="check_total_copies"),
    )

    # Relationships
    category = relationship("Category", back_populates="books")
    authors = relationship("Author", secondary="book_authors", back_populates="books")
    loans = relationship("Loan", back_populates="book")


# ─── MEMBER ──────────────────────────────────────────────────────────
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    join_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # One member has many loans
    loans = relationship("Loan", back_populates="member")


# ─── LOAN ────────────────────────────────────────────────────────────
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)  # NULL means still active

    # Relationships
    member = relationship("Member", back_populates="loans")
    book = relationship("Book", back_populates="loans")