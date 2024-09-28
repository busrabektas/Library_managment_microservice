# inventory_service/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, unique=True, index=True)  # Reference to book_service's Book ID
    quantity = Column(Integer, default=0)
