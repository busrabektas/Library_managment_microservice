from sqlalchemy.orm import Session
from . import models, schemas,database 
from datetime import datetime
from .producer import send_loan_event 



def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Loan).offset(skip).limit(limit).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = models.Loan(**loan.dict(), loan_date=datetime.now())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    
    
    
    
    
    return db_loan

def return_loan(db: Session, loan_id: int):
    db_loan = get_loan(db, loan_id)
    if db_loan:
        db_loan.return_date = datetime.now()
        db_loan.is_returned = True
        db.commit()
        db.refresh(db_loan)
    return db_loan
