from pydantic import BaseModel

class InventoryBase(BaseModel):
    book_id: int

class InventoryCreate(InventoryBase):
    quantity: int

class InventoryUpdate(BaseModel):
    quantity: int

class Inventory(InventoryBase):
    quantity: int

    class Config:
        from_attributes = True
