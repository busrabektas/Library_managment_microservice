from pydantic import BaseModel

class UserBase(BaseModel):
    full_name: str
    email: str
    age: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
