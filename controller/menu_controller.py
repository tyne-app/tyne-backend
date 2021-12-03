from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.orm import Session
from configuration.database import database
from dto.request.MenuRequestDTO import MenuRequestDTO
from service.JwtService import JwtService
from service.menu_service import MenuService

menu_controller = APIRouter(
    prefix="/v1/menus",
    tags=["Menus"]
)

_menu_service_ = MenuService()
_jwt_service = JwtService()


@menu_controller.get('/categories', status_code=status.HTTP_200_OK)
async def all_category(response: Response, db: Session = Depends(database.get_data_base)):
    categories = await _menu_service_.all_category(db)

    if categories is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return categories


@menu_controller.post('/{branch_id}', status_code=status.HTTP_201_CREATED)
async def create_menu(branch_id: int,
                      request: Request,
                      menu_request: MenuRequestDTO,
                      db: Session = Depends(database.get_data_base)):
    await _jwt_service.verify_and_get_token_data(request)
    return await _menu_service_.create_menu(branch_id, db, menu_request)


@menu_controller.get('/{branch_id}', status_code=status.HTTP_200_OK)
async def read_menu(branch_id: int,
                    response: Response,
                    db: Session = Depends(database.get_data_base)):
    menus = await _menu_service_.read_menu(branch_id, db)

    if menus is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return menus
