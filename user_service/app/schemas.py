from pydantic import BaseModel

class UserBase(BaseModel):
    id:int
    title: str
    author: str
    published_year: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
