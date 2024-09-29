# inventory_service/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager
import asyncio
import threading
import logging

from . import crud, models, schemas, database
from .consumer import consume_book_events, consume_loan_events

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db_session():
    return next(database.get_db())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Arka planda Kafka tüketicilerini başlatın
    book_consumer_thread = threading.Thread(target=consume_book_events, daemon=True)
    book_consumer_thread.start()
    logger.info("Inventory Service: Book Events Consumer thread started")

    loan_consumer_thread = threading.Thread(target=consume_loan_events, daemon=True)
    loan_consumer_thread.start()
    logger.info("Inventory Service: Loan Events Consumer thread started")

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/inventory/{book_id}", response_model=schemas.Inventory)
def read_inventory(book_id: int, db: Session = Depends(get_db_session)):
    inventory = crud.get_inventory(db, book_id=book_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@app.post("/inventory/", response_model=schemas.Inventory)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db_session)):
    existing_inventory = crud.get_inventory(db, book_id=inventory.book_id)
    if existing_inventory:
        raise HTTPException(status_code=400, detail="Inventory for this book already exists")
    return crud.create_inventory(db=db, inventory=inventory)

@app.put("/inventory/{book_id}", response_model=schemas.Inventory)
def update_inventory(book_id: int, inventory_update: schemas.InventoryUpdate, db: Session = Depends(get_db_session)):
    try:
        inventory = crud.update_inventory_quantity(db, book_id=book_id, quantity_change=inventory_update.quantity_change)
        if inventory is None:
            raise HTTPException(status_code=404, detail="Inventory not found or quantity reached zero")
        return inventory
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@app.delete("/inventory/{book_id}", response_model=schemas.Inventory)
def delete_inventory(book_id: int, db: Session = Depends(get_db_session)):
    inventory = crud.delete_inventory(db, book_id=book_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@app.get("/")
def read_root():
    return {"message": "Inventory Service is running!"}
