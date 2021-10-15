from domain2.Category import Category
from domain2.Menu import Menu
from domain2.Product import Product
from dto.dto import GenericDTO as wrapperDTO

from repository.entity.ProductEntity import ProductEntity


def to_menu_read_domain(products: list[ProductEntity]):
    menu_domain = Menu()

    for product in products:
        product_domain = Product(product.product_dict())
        category_domain = Category(product.get_category_dict())
        menu_domain.add_seccion(product_domain, category_domain)

    return menu_domain
