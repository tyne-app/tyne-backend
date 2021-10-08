from datetime import datetime

from dto.request.MenuRequestDTO import MenuRequestDTO, CategoryDTO
from repository.model.models import Category, Product, Price


def to_models_save(menu_request: MenuRequestDTO, branch_id):
    category_products_list_model = list()
    for menu, sections in menu_request:
        for section in sections:
            cat_model = to_category_model(section.category)
            products_model = to_products_model(section.products, branch_id)
            cat_model.product_category = products_model
            category_products_list_model.append(cat_model)

    return category_products_list_model


def to_category_model(category: CategoryDTO):
    category_model = Category(category.id, category.name)
    return category_model


def to_products_model(products, branch_id):
    products_model = list()

    for product in products:
        product_model = Product(product.id, product.name, product.description, product.url_image, branch_id)
        price_model = Price(amount=product.price, created_date=datetime.now())
        product_model.price_product.append(price_model)
        products_model.append(product_model)

    return products_model
