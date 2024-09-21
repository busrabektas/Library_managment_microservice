from sqlalchemy import Column, Integer, DateTime, Boolean
from .database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book_id = Column(Integer, index=True)
    loan_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
