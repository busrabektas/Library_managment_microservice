from sqlalchemy import Column, Integer
from .database import Base

class Inventory(Base):
    __tablename__ = 'inventory'

    book_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=0)
