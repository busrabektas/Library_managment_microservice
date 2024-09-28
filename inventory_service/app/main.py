# inventory_service/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager
import asyncio
import logging

from . import crud, models, schemas, database
# from .producer import send_inventory_update
# from .kafka_admin import create_kafka_topic
# from .consumer import consume_events

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app with lifespan
app = FastAPI()

# Create tables

# Dependency
def get_db_session():
    return database.get_db()

# Inventory Endpoints
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
    inventory = crud.update_inventory(db, book_id=book_id, quantity=inventory_update.quantity)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@app.delete("/inventory/{book_id}", response_model=schemas.Inventory)
def delete_inventory(book_id: int, db: Session = Depends(get_db_session)):
    inventory = crud.delete_inventory(db, book_id=book_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@app.get("/")
def read_root():
    return {"message": "Inventory Service is running!"}
