from fastapi import APIRouter, Depends, Response, status
from loguru import logger
from sqlalchemy.orm import Session

from dto.dto import GenericDTO as ResponseDTO
from dto.request.MenuRequestDTO import MenuRequestDTO
from exception.exceptions import CustomError
from mappers.request import menu_mapper_request
from mappers.response import menu_mapper_response
from repository.dao import menu_dao
from repository.database.database import get_data_base
from repository.model.models import Product

menu_router = APIRouter(
    prefix="/v1/locals/menu",
    tags=["Menu"]
)


#  Se creará el menu por productos
# async def create_menu(menuRequest: MenuRequest, response: Response):
@menu_router.post('/{branch_id}', status_code=status.HTTP_201_CREATED)
async def create_menu(branch_id: int, response: Response, menu_request: MenuRequestDTO,
                      db: Session = Depends(get_data_base)):
    response = ResponseDTO()
    logger.info('branch_id: {}', menu_request)

    models = menu_mapper_request.to_models_save(menu_request, branch_id)

    if menu_dao.save(db, models):
        response.data = [{"details": "Productos y categorias guardados correctamente"}]
        return response


#  Se modificará el menu por productos
@menu_router.put('/{branch_id}', status_code=status.HTTP_201_CREATED)
async def update_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)
    return "GUARDA CAMBIOS DE MENUS"


# @menu_router.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
@menu_router.get('/{branch_id}', status_code=status.HTTP_200_OK)  # Obtiene el menu según la sucursal
async def read_menu(branch_id: int, response: Response, db: Session = Depends(get_data_base)):
    products: list[Product] = menu_dao.get_products_by_branch(db, branch_id)

    if not products:
        raise CustomError(
            name="Products not Found",
            detail="No Products for menu",
            status_code=status.HTTP_204_NO_CONTENT)

    menu_response = menu_mapper_response.to_menu_response(products)

    return menu_response


"""#  Obtiene las categorías del menú
@menu_router.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
async def read_category_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)

    data = await get_menu(branch_id=branch_id)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data"""

#  Se eliminará el menú
# @menu_router.delete('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
# async def delete_menu(branch_id: int, response: Response):
#     logger.info('branch_id: {}', branch_id)
#
#     data = await get_menu(branch_id=branch_id)
#
#     if 'data' not in data:
#         response.status_code = status.HTTP_400_BAD_REQUEST
#
#     return data


# Se sacará el producto del menú
# @menu_router.delete('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
# async def delete_product_menu(branch_id: int, response: Response):
#     logger.info('branch_id: {}', branch_id)
#
#     data = await get_menu(branch_id=branch_id)
#
#     if 'data' not in data:
#         response.status_code = status.HTTP_400_BAD_REQUEST
#
#     return data
