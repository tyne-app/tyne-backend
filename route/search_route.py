from fastapi import status,APIRouter, Response
from fastapi.params import Depends
from typing import Optional
from loguru import logger
from schema.search_schema import SearchParameters
from domain.search_domain import search_all_branch

search_router = APIRouter(
    prefix="/v1/api/search",
    tags=["Search"]
)


@search_router.post('/all-branch', status_code=status.HTTP_200_OK)
async def search_locals(response: Response, search_parameters: SearchParameters):
    logger.info('search_paramters: {}', search_parameters)

    data = search_all_branch(search_parameters=search_parameters)
    print(data)
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
