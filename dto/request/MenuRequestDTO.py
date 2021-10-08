from typing import Optional

from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: Optional[str]
    name: str
    description: str
    url_image: str
    price: str


class CategoryDTO(BaseModel):
    id: Optional[str]
    name: str


class SectionMenuDTO(BaseModel):
    category: CategoryDTO
    products: list[ProductDTO]


class MenuRequestDTO(BaseModel):
    menu: list[SectionMenuDTO]
