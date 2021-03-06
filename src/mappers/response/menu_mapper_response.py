from src.domain2.Menu import Menu
from src.repository.entity.ProductEntity import ProductEntity


def to_menu_read_response(products: list[ProductEntity], branch, categories):
    menu = Menu()
    return menu.to_menu_read_domain(products, branch, categories)


def to_menu_create_response():
    return {"message": "Menu creado correctamente"}
