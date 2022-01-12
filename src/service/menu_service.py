from sqlalchemy.orm import Session
from starlette import status

from src.dto.response.CategoryResponse import CategoryResponse
from src.mappers.request import menu_mapper_request
from src.mappers.response import menu_mapper_response
from src.repository.dao.BranchDao import BranchDao
from src.repository.dao.CategoryDao import CategoryDao
from src.repository.dao.OpinionDao import OpinionDao
from src.repository.dao.ProductDao import ProductDao
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.ProductEntity import ProductEntity
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions


class MenuService:
    _opinion_dao = OpinionDao()
    _thrower_exceptions = ThrowerExceptions()
    _category_dao_ = CategoryDao()
    _branch_dao_ = BranchDao()
    _product_dao_ = ProductDao()

    async def create_menu(self, branch_id, db, menu_request):
        seccions_list_entity = menu_mapper_request.to_entities(menu_request, branch_id)

        is_saved = self._product_dao_.save_all_products_menu(db, seccions_list_entity, branch_id)

        if not is_saved:
            await self._thrower_exceptions.throw_custom_exception(name=Constants.MENU_CREATE_ERROR,
                                                                  detail=Constants.MENU_CREATE_ERROR,
                                                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        menu_response = menu_mapper_response.to_menu_create_response()

        return menu_response

    async def read_menu(self, branch_id, db):
        products: list[ProductEntity] = self._product_dao_.get_products_by_branch(db, branch_id)
        branch: BranchEntity = self._branch_dao_.get_branch_by_id(db, branch_id)
        opinions = self._opinion_dao.find_by_branch_id(db, branch_id)

        if not products:
            return None

        menu_read_response = menu_mapper_response.to_menu_read_response(products, branch, opinions)

        return menu_read_response

    async def all_category(self, db: Session):
        categories = self._category_dao_.get_categories(db=db)
        category_response = CategoryResponse()
        response = category_response.to_all_categories(categories)
        return response