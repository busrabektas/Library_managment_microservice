# inventory_service/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_inventory(db: Session, book_id: int):
    return db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()

def create_inventory(db: Session, inventory: schemas.InventoryCreate):
    db_inventory = models.Inventory(book_id=inventory.book_id, quantity=inventory.quantity)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory(db: Session, book_id: int, quantity: int):
    db_inventory = db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()
    if db_inventory:
        db_inventory.quantity = quantity
        db.commit()
        db.refresh(db_inventory)
    return db_inventory

def delete_inventory(db: Session, book_id: int):
    db_inventory = db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()
    if db_inventory:
        db.delete(db_inventory)
        db.commit()
    return db_inventory
