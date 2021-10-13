from loguru import logger
from starlette import status

from exception.exceptions import CustomError
from mappers.request import menu_mapper_request
from mappers.response import menu_mapper_response
from repository.dao import product_dao, category_dao
from repository.entity.ProductEntity import ProductEntity


async def create_menu(branch_id, db, menu_request):
    logger.info('menu_request - create_menu: {}', menu_request)

    # TODO: Validator

    seccions_list_entity = menu_mapper_request.to_entities(menu_request, branch_id)

    for products in seccions_list_entity:
        is_saved = product_dao.save_all_products(db, products, 3)

        if not is_saved:
            raise CustomError(
                name="Error in create_menu",
                detail="Products not created or updated",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    menu_response = menu_mapper_response.to_menu_create_response()
    logger.info('menu_response - create_menu: {}', menu_response)
    return menu_response


async def read_menu(branch_id, db):
    logger.info('menu_request - read_menu branch_id: {}', branch_id)

    products: list[ProductEntity] = product_dao.get_products_by_branch(db, branch_id)

    if not products:
        raise CustomError(
            name="Products not Found",
            detail="No Products for menu",
            status_code=status.HTTP_204_NO_CONTENT)

    menu_response = menu_mapper_response.to_menu_read_response(products)

    logger.info('menu_response - read_menu: {}', menu_response)

    return menu_response
