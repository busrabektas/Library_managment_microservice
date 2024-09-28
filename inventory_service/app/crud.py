from sqlalchemy.orm import Session

from app.models import Book

from app.schemas import BookCreate

from . import models


def create_book(db: Session, book: BookCreate):
    db_book = models.Book(title=book.title, author=book.author, isbn=book.isbn, quantity=book.quantity)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book_quantity(db: Session, book_id: int, quantity: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db_book.quantity = quantity
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
