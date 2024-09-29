import threading
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .consumer import consume_user_events, consume_loan_events
from . import crud, models, schemas, database
from .producer import send_loan_event
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


models.Base.metadata.create_all(bind=database.engine)

def get_db_session():
    return next(database.get_db())

@asynccontextmanager
async def lifespan(app: FastAPI):
    user_consumer_thread = threading.Thread(target=consume_user_events, daemon=True)
    user_consumer_thread.start()
    logger.info("Loan Service: User Events Consumer thread started")

    loan_consumer_thread = threading.Thread(target=consume_loan_events, daemon=True)
    loan_consumer_thread.start()
    logger.info("Loan Service: Loan Events Consumer thread started")

    yield
app = FastAPI(lifespan=lifespan)


@app.post("/loans", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db_session)):
    created_loan = crud.create_loan(db=db, loan=loan)
    send_loan_event('BOOK_LOANED', {
        'user_id': loan.user_id,
        'book_id': loan.book_id,
        'loan_id': created_loan.id
    })
    logger.info(f"Loan created: {created_loan}")

    return created_loan

@app.get("/loans", response_model=List[schemas.Loan])
def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    loans = crud.get_loans(db, skip=skip, limit=limit)
    return loans

@app.get("/loans/{loan_id}", response_model=schemas.Loan)
def read_loan(loan_id: int, db: Session = Depends(get_db_session)):
    loan = crud.get_loan(db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@app.put("/loans/{loan_id}/return", response_model=schemas.Loan)
def return_loan(loan_id: int, db: Session = Depends(get_db_session)):
    loan = crud.return_loan(db=db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    send_loan_event('BOOK_RETURNED', {
        'loan_id': loan.id,
        'book_id': loan.book_id
    })
    logger.info(f"Loan returned: {loan}")

    return loan

@app.get("/")
def read_root():
    return {"message": "Loan Service is running!"}
