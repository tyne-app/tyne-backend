from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.orm import Session

from configuration.database import database
from dto.request.MenuRequestDTO import MenuRequestDTO
from exception.exceptions import CustomError
from service import menu_service
from loguru import logger

menu_controller = APIRouter(
    prefix="/v1/menus",
    tags=["Menus"]
)


@menu_controller.get('/categories', status_code=status.HTTP_200_OK)
async def all_category(db: Session = Depends(database.get_data_base)):
    return await menu_service.all_category(db)


#  Se creará el menu por productos
@menu_controller.post('/{branch_id}', status_code=status.HTTP_201_CREATED)
async def create_menu(branch_id: int,
                      request: Request,
                      response: Response,
                      menu_request: MenuRequestDTO,
                      db: Session = Depends(database.get_data_base)):
    if 'authorization' not in request.headers:
        # TODO: Refactor
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    return await menu_service.create_menu(branch_id, db, menu_request)


# Obtiene el menu según la sucursal
@menu_controller.get('/{branch_id}', status_code=status.HTTP_200_OK)
async def read_menu(branch_id: int,
                    response: Response,
                    db: Session = Depends(database.get_data_base)):
    return await menu_service.read_menu(branch_id, db)
