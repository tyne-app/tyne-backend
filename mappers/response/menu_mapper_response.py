from domain2.Menu import Menu

from repository.entity.BranchEntity import BranchEntity
from repository.entity.ProductEntity import ProductEntity


def to_menu_read_response(products: list[ProductEntity], branch: BranchEntity, opinions):
    return Menu.to_menu_read_domain(products, branch, opinions)


def to_menu_create_response():
    return {"message": "Menu creado correctamente"}
