from typing import Optional, Union
from pydantic import BaseModel


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


class MenuResponse(BaseModel):
    id: str
    product_id: str
    branch_id: str


class MenuOutput(BaseModel):
    # data: Optional[list] = []
    # error: Optional[str] = []
    data: Optional[MenuResponse] = []
    error: Optional[str] = []
