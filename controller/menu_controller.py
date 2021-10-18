from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from configuration.database import database
from dto.request.MenuRequestDTO import MenuRequestDTO
from dto.response.MenuRespDTO import MenuRespDTO, MenuRespOutput
from exception.exceptions import CustomError
from service import menu_service
from loguru import logger

menu_controller = APIRouter(
    prefix="/v1/locals/menu",
    tags=["Menu"]
)


#  Se creará el menu por productos
@menu_controller.post('/{branch_id}', status_code=status.HTTP_201_CREATED)
async def create_menu(branch_id: int,
                      response: Response,
                      menu_request: MenuRequestDTO,
                      db: Session = Depends(database.get_data_base)):

    try:
        return await menu_service.create_menu(branch_id, db, menu_request)

    except CustomError as error:
        logger.error(error.detail)
        raise CustomError(name=error.name,
                          detail=error.detail,
                          status_code=error.status_code,
                          cause=error.cause)

    except Exception as error:
        logger.error(error)
        raise CustomError(name="Error create_menu",
                          detail="Controller error",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          cause=error.__cause__)


# Obtiene el menu según la sucursal
@menu_controller.get('/{branch_id}', status_code=status.HTTP_200_OK)
async def read_menu(branch_id: int,
                    response: Response,
                    db: Session = Depends(database.get_data_base)):
    try:
        return await menu_service.read_menu(branch_id, db)

    except CustomError as error:
        logger.error(error.detail)
        raise CustomError(name=error.name,
                          detail=error.detail,
                          status_code=error.status_code,
                          cause=error.cause)

    except Exception as error:
        logger.error(error)
        raise CustomError(name="Error read_menu",
                          detail="Controller error",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          cause=error.__cause__)

