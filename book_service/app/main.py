from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from . import crud, schemas
from . import models,database
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)


# Pydantic Model
class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int



@app.post("/books", response_model=schemas.Book)
def create_book(item: schemas.BookCreate, db: Session = Depends(database.get_db)):
    return crud.create_book(db=db, item=item)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_book

@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, item: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = crud.update_book(db=db, book_id=book_id, item=item)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/")
def read_root():
    return {"message": "Book Service is running!"}
