from src.exception.exceptions import CustomError
from src.util.Constants import Constants
from starlette import status
from loguru import logger
from src.dto.request.MenuRequestDTO import SectionMenuDTO


class MenuValidator:

    def list_has_product(self, menu_list: list) -> None:
        logger.info("menu_list: {}", menu_list)

        section: SectionMenuDTO
        for section in menu_list:
            print(section)
            if not section.products:
                raise CustomError(name=Constants.MENU_CREATE_ERROR,
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  detail=Constants.MENU_CREATE_ERROR_DETAIL,
                                  cause=Constants.MENU_CREATE_ERROR)