from dto.dto import GenericDTO as wrapperDTO
from dto.response.MenuResponseDTO import MenuDTO, ProductDTO, CategoryDTO
from repository.model.models import Product


def to_menu_response(products: list[Product]):
    wrapper_response = wrapperDTO()
    menu = MenuDTO()

    for product in products:
        productDto = ProductDTO(product.product_dict())
        category = CategoryDTO(product.get_category_dict())
        menu.add_seccion(productDto, category)

    wrapper_response.data = menu

    return wrapper_response.__dict__
