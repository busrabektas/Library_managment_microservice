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

def update_inventory_quantity(db: Session, book_id: int, quantity_change: int):

    db_inventory = db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()
    if db_inventory:
        new_quantity = db_inventory.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Yetersiz stok miktarı.")
        db_inventory.quantity = new_quantity
        db.commit()
        db.refresh(db_inventory)
        if db_inventory.quantity == 0:
            db.delete(db_inventory)
            db.commit()
            return None  
        return db_inventory
    else:
        raise ValueError("Envanter bulunamadı.")

def delete_inventory(db: Session, book_id: int):
    db_inventory = db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()
    if db_inventory:
        db.delete(db_inventory)
        db.commit()
    return db_inventory
