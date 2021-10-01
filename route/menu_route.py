from typing import Optional, Union
from fastapi import status, APIRouter, Response, Request
from loguru import logger
from domain.menu_domain import get_menu
from schema.menu_schema import MenuOutput, MenuRequest

menu_router = APIRouter(
    prefix="/v1/locals/menu",
    tags=["Menu"]
)


#  Se creará el menu por productos
@menu_router.post('/{branch_id}', status_code=status.HTTP_200_OK)
async def create_menu(menuRequest: MenuRequest, response: Response):
    # logger.info('branch_id: {}', branch_id)

    return 'TODOS LOS MENUS en desarrollo'


#  Se modificará el menu por productos
@menu_router.put('/{branch_id}', status_code=status.HTTP_200_OK)
async def update_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)
    return "GUARDA CAMBIOS DE MENUS"


#  Obtiene el menu según la sucursal
@menu_router.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
async def read_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)

    data = await get_menu(branch_id=branch_id)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


#  Obtiene las categorías del menú
@menu_router.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
async def read_category_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)

    data = await get_menu(branch_id=branch_id)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


#  Se eliminará el menú
@menu_router.delete('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
async def delete_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)

    data = await get_menu(branch_id=branch_id)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


# Se sacará el producto del menú
@menu_router.delete('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
async def delete_product_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)

    data = await get_menu(branch_id=branch_id)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
