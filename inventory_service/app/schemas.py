from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    quantity: int

    class Config:
        orm_mode = True

class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    quantity: int

    class Config:
        orm_mode = True
