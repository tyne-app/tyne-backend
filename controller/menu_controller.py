from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from configuration.database import database
from dto.request.MenuRequestDTO import MenuRequestDTO
from dto.response.MenuResponseDTO import MenuResponseDTO
from service import menu_service

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
    return await menu_service.create_menu(branch_id, db, menu_request)


# Obtiene el menu según la sucursal
@menu_controller.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuResponseDTO)
async def read_menu(branch_id: int,
                    response: Response,
                    db: Session = Depends(database.get_data_base)):
    return await menu_service.read_menu(branch_id, db)
