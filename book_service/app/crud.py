from sqlalchemy.orm import Session
from . import models, schemas

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, item: schemas.BookCreate):
    db_book = models.Book(id=item.id, title=item.title, author=item.author, published_year=item.published_year )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, item: schemas.BookCreate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db_book.title = item.title
        db_book.author = item.author
        db_book.published_year = item.published_year
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
