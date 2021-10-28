from loguru import logger
from starlette import status

from dto.response.CategoryResponse import CategoryResponse
from exception.exceptions import CustomError
from mappers.request import menu_mapper_request
from mappers.response import menu_mapper_response
from repository.dao import ProductDao, CategoryDao, branch_dao
from repository.entity.BranchEntity import BranchEntity
from repository.entity.ProductEntity import ProductEntity


async def create_menu(branch_id, db, menu_request):
    logger.info('menu_request - create_menu: {}', menu_request)

    seccions_list_entity = menu_mapper_request.to_entities(menu_request, branch_id)

    is_saved = ProductDao.save_all_products_menu(db, seccions_list_entity, branch_id)

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

    products: list[ProductEntity] = ProductDao.get_products_by_branch(db, branch_id)
    branch: BranchEntity = branch_dao.get_branch_by_id(db, branch_id)

    if not products:
        raise CustomError(
            name="Products not Found",
            detail="No Products for menu",
            status_code=status.HTTP_204_NO_CONTENT)

    menu_read_response = menu_mapper_response.to_menu_read_response(products, branch)

    return menu_read_response


async def all_category(db):
    logger.info('menu_request - all_category')
    categories = CategoryDao.get_all(db)

    if not categories:
        raise CustomError(
            name="categories not Found",
            detail="No categories",
            status_code=status.HTTP_204_NO_CONTENT)

    category_response = CategoryResponse()
    response = category_response.to_all_categories(categories)

    return response
