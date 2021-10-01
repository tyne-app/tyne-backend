from typing import Optional, Union
from pydantic import BaseModel


class MenuOutput(BaseModel):
    data: Optional[list] = []
    error: Optional[str] = []


class Product(BaseModel):
    id: str
    name: str
    price: str
    description: str
    image_url: str


class Category(BaseModel):
    id: str
    name: str
    products: list[Product]


class MenuRequest(BaseModel):
    branchId: str
    categories: list[Category]
