from typing import Optional
from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: Optional[str]
    name: str
    description: str
    url_image: Optional[str]
    amount: int


class SectionMenuDTO(BaseModel):
    category_id: int
    products: list[ProductDTO]


class MenuRequestDTO(BaseModel):
    menu: list[SectionMenuDTO]
