from pydantic import BaseModel
from typing import List
from datetime import datetime
from Schemas.user import UserInOrder
from Schemas.product import ProductInOrder

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float
    product: ProductInOrder

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    user: UserInOrder
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
