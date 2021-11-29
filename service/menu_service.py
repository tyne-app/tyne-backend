from starlette import status

from dto.response.CategoryResponse import CategoryResponse
from mappers.request import menu_mapper_request
from mappers.response import menu_mapper_response
from repository.dao import ProductDao, CategoryDao, branch_dao
from repository.dao.OpinionDao import OpinionDao
from repository.entity.BranchEntity import BranchEntity
from repository.entity.ProductEntity import ProductEntity
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions

_opinion_dao = OpinionDao()
_throwerExceptions = ThrowerExceptions()


async def create_menu(branch_id, db, menu_request):
    seccions_list_entity = menu_mapper_request.to_entities(menu_request, branch_id)

    is_saved = ProductDao.save_all_products_menu(db, seccions_list_entity, branch_id)

    if not is_saved:
        await _throwerExceptions.throw_custom_exception(name=Constants.MENU_CREATE_ERROR,
                                                        detail=Constants.MENU_CREATE_ERROR,
                                                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    menu_response = menu_mapper_response.to_menu_create_response()

    return menu_response


async def read_menu(branch_id, db):
    products: list[ProductEntity] = ProductDao.get_products_by_branch(db, branch_id)
    branch: BranchEntity = branch_dao.get_branch_by_id(db, branch_id)
    opinions = _opinion_dao.find_by_branch_id(db, branch_id)

    if not products:
        await _throwerExceptions.throw_custom_exception(name=Constants.MENU_READ_ERROR,
                                                        detail=Constants.MENU_READ_ERROR_DETAIL,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    menu_read_response = menu_mapper_response.to_menu_read_response(products, branch, opinions)

    return menu_read_response


async def all_category(db):
    categories = CategoryDao.get_all(db)

    if not categories:
        await _throwerExceptions.throw_custom_exception(name=Constants.MENU_ALL_CATEGORY_ERROR,
                                                        detail=Constants.MENU_ALL_CATEGORY_ERROR_DETAIL,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    category_response = CategoryResponse()
    response = category_response.to_all_categories(categories)

    return response
