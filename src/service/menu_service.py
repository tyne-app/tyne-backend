from sqlalchemy.orm import Session
from loguru import logger
from src.dto.response.CategoryResponse import CategoryResponse
from src.mappers.request.MenuMapperRequest import MenuMapperRequest
from src.mappers.response import menu_mapper_response
from src.repository.dao.BranchDao import BranchDao
from src.repository.dao.CategoryDao import CategoryDao
from src.repository.dao.ProductDao import ProductDao
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.ProductEntity import ProductEntity
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.dto.request.MenuRequestDTO import MenuRequestDTO
from src.validator.MenuValidator import MenuValidator


class MenuService:
    _thrower_exceptions = ThrowerExceptions()
    _category_dao_ = CategoryDao()
    _branch_dao_ = BranchDao()
    _product_dao_ = ProductDao()
    _menu_validator = MenuValidator()
    _menu_mapper_request = MenuMapperRequest()

    async def create_menu(self, branch_id, db, menu_request: MenuRequestDTO):
        logger.info("branch_id: {}, menu_request: {}", branch_id, menu_request)

        self._menu_validator.list_has_product(menu_list=menu_request.menu)

        sections_list_entity = self._menu_mapper_request.to_entities(menu_request, branch_id)
        logger.info("seccions_list_entity: {}", sections_list_entity)

        self._product_dao_.save_all_products_menu(db, sections_list_entity, branch_id)

        return menu_mapper_response.to_menu_create_response()

    async def read_menu(self, branch_id, db):
        products: list[ProductEntity] = self._product_dao_.get_products_by_branch(db, branch_id)
        branch: BranchEntity = self._branch_dao_.get_branch_by_id(db, branch_id)

        if not products:
            return None

        menu_read_response = menu_mapper_response.to_menu_read_response(products, branch)

        return menu_read_response

    async def all_category(self, db: Session):
        categories = self._category_dao_.get_categories(db=db)
        category_response = CategoryResponse()
        response = category_response.to_all_categories(categories)
        return response
