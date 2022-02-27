from typing import Optional, Union
from pydantic import BaseModel


class ProductRespDTO(BaseModel):
    id: str
    name: str
    description: str
    url_image: str
    amount: str
    commission_tyne: str


class CategoryRespDTO(BaseModel):
    id: str
    name: str


class SectionMenuRespDTO(BaseModel):
    category: CategoryRespDTO
    products: list[ProductRespDTO]


class MenuRespDTO(BaseModel):
    sections: list[SectionMenuRespDTO]


class MenuRespOutput(BaseModel):
    data: Optional[Union[MenuRespDTO, list]] = []
    error: Optional[Union[str, dict, list]] = []
