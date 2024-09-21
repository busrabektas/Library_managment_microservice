from sqlalchemy import Column, Integer, String
from app.database import Base

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    isbn = Column(String(255), unique=True, index=True)
    quantity = Column(Integer)
