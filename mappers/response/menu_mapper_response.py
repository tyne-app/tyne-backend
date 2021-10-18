from domain2.Category import Category
from domain2.Menu import Menu
from domain2.Product import Product
from domain2.SectionMenu import SectionMenu
from dto.dto import GenericDTO as wrapperDTO

from dto.response.MenuRespDTO import MenuRespDTO, CategoryRespDTO, SectionMenuRespDTO, ProductRespDTO
from repository.entity.ProductEntity import ProductEntity


def to_menu_read_response(products: list[ProductEntity]):
    menu_domain = Menu()

    for product in products:
        product_domain = Product(product.product_dict())
        category_domain = Category(product.get_category_dict())
        menu_domain.add_seccion(product_domain, category_domain)

    return menu_domain


def to_menu_create_response():
    response = wrapperDTO()
    response.data = [{"message": "Menu creado correctamente"}]
    return response.__dict__
