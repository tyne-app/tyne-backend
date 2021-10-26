from domain2.Category import Category
from domain2.Menu import Menu
from domain2.Product import Product
from dto.dto import GenericDTO as wrapperDTO
from dto.response.CategoryResponse import CategoryResponse
from repository.entity.BranchEntity import BranchEntity

from repository.entity.ProductEntity import ProductEntity
from repository.entity.CategoryEntity import CategoryEntity


def to_menu_read_domain(products: list[ProductEntity], branch: BranchEntity):
    menu_domain = Menu(branch.id, branch.description)
    price_set = list()

    for product in products:
        product_domain = Product(product.product_dict())
        category_domain = Category(product.get_category_dict())
        menu_domain.add_seccion(product_domain, category_domain)
        price_set.append(product.amount)

    max_amount = max(price_set, key=float)
    min_amount = min(price_set, key=float)
    avg_amount = sum(price_set) / len(price_set)

    menu_domain.rango_precio = {
        "max": max_amount,
        "min": min_amount,
        "avg": avg_amount,
    }

    return menu_domain

