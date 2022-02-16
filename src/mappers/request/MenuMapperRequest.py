from src.dto.request.MenuRequestDTO import MenuRequestDTO
from src.repository.entity.ProductEntity import ProductEntity


class MenuMapperRequest:
    _ELEMENT_INDEX = 1

    def to_entities(self, menu_request: MenuRequestDTO, branch_id) -> list:
        sections_list_entity: list = []

        for category_id, products in menu_request.menu:
            products_list_entity: list = self.to_products_entity(products[self._ELEMENT_INDEX],
                                                                 branch_id, category_id[self._ELEMENT_INDEX])
            sections_list_entity.append(products_list_entity)
        return sections_list_entity

    def to_products_entity(self, products, branch_id, category_id) -> list:
        products_list_entity = list()
        for product in products:
            product_entity = ProductEntity(product.id, category_id, product.name, product.description,
                                           product.url_image, product.amount, branch_id)
            products_list_entity.append(product_entity)
        return products_list_entity
