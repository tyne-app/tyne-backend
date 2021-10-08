from typing import Optional, Union
from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    description: str
    image_url: str
    price: str


class Category(BaseModel):
    id: str
    name: str
    products: list[Product]

    class Config:
        orm_mode = True


class MenuRequest(BaseModel):
    branchId: str
    categories: list[Category]


class MenuResponse(BaseModel):
    id: int
    product_id: int
    branch_id: int

    class Config:
        orm_mode = True


class MenuOutput(BaseModel):
    data: Optional[str] = []
    error: Optional[str] = []
