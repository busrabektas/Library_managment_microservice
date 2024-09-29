from pydantic import BaseModel

class BookBase(BaseModel):
    id: int
    title: str
    author: str
    published_year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True  