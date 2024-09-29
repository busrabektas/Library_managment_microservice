from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Loan).offset(skip).limit(limit).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = models.Loan(
        user_id=loan.user_id,
        book_id=loan.book_id,
        loan_date=datetime.now(timezone.utc),
        is_returned=False
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def return_loan(db: Session, loan_id: int):
    db_loan = get_loan(db, loan_id)
    if db_loan and not db_loan.is_returned:
        db_loan.return_date = datetime.now(timezone.utc)
        db_loan.is_returned = True
        db.commit()
        db.refresh(db_loan)
    return db_loan

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_inventory_quantity(db: Session, book_id: int, quantity_change: int):

    try:
        db_inventory = db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()
        if not db_inventory:
            raise ValueError("Envanter bulunamadı.")

        new_quantity = db_inventory.quantity + quantity_change

        if new_quantity < 0:
            raise ValueError("Yetersiz stok miktarı.")

        db_inventory.quantity = new_quantity
        db.commit()
        db.refresh(db_inventory)

        if db_inventory.quantity == 0:
            db.delete(db_inventory)
            db.commit()
            logger.info(f"Inventory for book ID {book_id} silindi çünkü stok miktarı sıfırlandı.")
            return None

        logger.info(f"Inventory for book ID {book_id} güncellendi, yeni miktar: {db_inventory.quantity}")
        return db_inventory

    except Exception as e:
        logger.error(f"Inventory update error for book ID {book_id}: {e}")
        raise e
