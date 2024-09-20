from sqlalchemy import Column, Integer, String
from .database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    published_year = Column(Integer)
