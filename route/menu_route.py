from typing import Optional, Union
from fastapi import status, APIRouter, Response, Request
from loguru import logger
from domain.menu_domain import get_menu
from schema.menu_schema import MenuOutput

menu_router = APIRouter(
    prefix="/v1/api/menu",
    tags=["Menu"]
)


@menu_router.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=MenuOutput)
async def read_menu(branch_id: int, response: Response):
    logger.info('branch_id: {}', branch_id)

    data = await get_menu(branch_id=branch_id)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
