from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    quantity: int

    class Config:
        from_attributes = True


class Book(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    quantity: int

    class Config:
        from_attributes = True  # orm_mode yerine bunu kullanın