from fastapi import status,APIRouter, Response, Body
from loguru import logger
from schema.search_schema import SearchParameters, PreviewBranchOutput
from domain.search_domain import search_all_branch

search_router = APIRouter(
    prefix="/v1/api/search",
    tags=["Search"]
)


@search_router.post('/all-branch', status_code=status.HTTP_200_OK, response_model=PreviewBranchOutput)
async def search_locals(response: Response, search_parameters: SearchParameters = Body(default = {})):
    logger.info('search_paramters: {}', search_parameters)

    data = await search_all_branch(search_parameters=search_parameters)
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@search_router.post('/all-branch/{client_id}', status_code=status.HTTP_200_OK)
async def search_locals_client(response: Response, search_parameters: SearchParameters, client_id: int):
    logger.info('search_paramters: {}', search_parameters)

    data = await search_all_branch(search_parameters=search_parameters, client_id=client_id)
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
