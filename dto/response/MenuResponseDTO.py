from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: str
    name: str
    description: str
    url_image: str
    amount: str
    commision_tyne: str


class CategoryDTO(BaseModel):
    id: str
    name: str


class SectionMenuDTO(BaseModel):
    category: CategoryDTO
    products: list[ProductDTO]


class MenuResponseDTO(BaseModel):
    menu: list[SectionMenuDTO]
