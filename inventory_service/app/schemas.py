# inventory_service/schemas.py

from pydantic import BaseModel

class InventoryBase(BaseModel):
    book_id: int
    quantity: int

    class Config:
        orm_mode = True

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: int

    class Config:
        orm_mode = True

class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True
