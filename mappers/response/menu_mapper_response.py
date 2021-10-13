from domain2.Category import Category
from domain2.Menu import Menu
from domain2.Product import Product
from dto.dto import GenericDTO as wrapperDTO

from repository.entity.ProductEntity import ProductEntity


def to_menu_read_response(products: list[ProductEntity]):
    wrapper_response = wrapperDTO()
    menu_domain = Menu()

    for product in products:
        product_domain = Product(product.product_dict())
        category_domain = Category(product.get_category_dict())
        menu_domain.add_seccion(product_domain, category_domain)

    wrapper_response.data = menu_domain

    return wrapper_response.__dict__


def to_menu_create_response():
    wrapper_response = wrapperDTO()
    menu = Menu()

    wrapper_response.data = [{"details": "Productos guardados correctamente"}]

    return wrapper_response.__dict__
