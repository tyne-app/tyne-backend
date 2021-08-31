from fastapi import status,APIRouter, Response, Body
from loguru import logger
from schema.search_schema import SearchParameters, PreviewBranchOutput, PreviewBranchOutputClient
from domain.search_domain import search_all_branch
from openapi.search_openapi import SearchAllBranchByClientOpenAPI, SearchAllBranchOpenAPI

search_router = APIRouter(
    prefix="/v1/api/search",
    tags=["Search"]
)


@search_router.post(
    '/all-branch', status_code=status.HTTP_200_OK, response_model=PreviewBranchOutput,
    summary=SearchAllBranchOpenAPI.summary, responses=SearchAllBranchOpenAPI.responses,
    description=SearchAllBranchOpenAPI.description, response_description=SearchAllBranchOpenAPI.response_description
)
async def search_locals(response: Response, search_parameters: SearchParameters = Body(default = {})):
    logger.info('search_paramters: {}', search_parameters)

    data = await search_all_branch(search_parameters=search_parameters)
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@search_router.post(
    '/all-branch/{client_id}', status_code=status.HTTP_200_OK, response_model=PreviewBranchOutputClient,
    summary=SearchAllBranchByClientOpenAPI.summary, responses=SearchAllBranchByClientOpenAPI.responses,
    description=SearchAllBranchByClientOpenAPI.description, response_description=SearchAllBranchByClientOpenAPI.response_description
)
async def search_locals_client(response: Response, client_id: int, search_parameters: SearchParameters = Body(default = {})):
    logger.info('search_paramters: {}', search_parameters)

    data = await search_all_branch(search_parameters=search_parameters, client_id=client_id)
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
