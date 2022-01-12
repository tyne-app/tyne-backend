from src.dto.request.MenuRequestDTO import MenuRequestDTO, CategoryDTO
from src.repository.entity.CategoryEntity import CategoryEntity
from src.repository.entity.ProductEntity import ProductEntity


def to_entities(menu_request: MenuRequestDTO, branch_id):
    seccions_list_entity = list()

    for menu, sections in menu_request:
        for section in sections:
            cat_entity = to_category_entity(section.category)
            products_list_entity = to_products_entity(section.products, branch_id, cat_entity.id)
            seccions_list_entity.append(products_list_entity)

    return seccions_list_entity


def to_category_entity(category: CategoryDTO):
    category_model = CategoryEntity(category.id, category.name)
    return category_model


def to_products_entity(products, branch_id, category_id):
    products_list_entity = list()
    for product in products:
        product_entity = ProductEntity(product.id, category_id, product.name, product.description, product.url_image, product.amount, product.commission_tyne, branch_id)
        products_list_entity.append(product_entity)
    return products_list_entity
