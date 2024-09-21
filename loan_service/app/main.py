from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

@app.post("/loans", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(database.get_db)):
    return crud.create_loan(db=db, loan=loan)

@app.get("/loans", response_model=List[schemas.Loan])
def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    loans = crud.get_loans(db, skip=skip, limit=limit)
    return loans

@app.get("/loans/{loan_id}", response_model=schemas.Loan)
def read_loan(loan_id: int, db: Session = Depends(database.get_db)):
    loan = crud.get_loan(db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@app.put("/loans/{loan_id}/return", response_model=schemas.Loan)
def return_loan(loan_id: int, db: Session = Depends(database.get_db)):
    loan = crud.return_loan(db=db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
