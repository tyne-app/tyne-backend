from fastapi import status,APIRouter, Response, Body, Request
from loguru import logger
from schema.search_schema import SearchParameters, PreviewBranchOutput, PreviewBranchOutputClient
from domain.search_domain import search_all_branch, validate_token
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

# TODO: Parece que se deberá ocupar un decorador, middleware se ejecuta antes del routing.
# https://stackoverflow.com/questions/62895883/fastapi-cant-access-path-parameters-from-middleware
# https://gist.github.com/geospatial-jeff/17d677202f1223eacd3b32960ac29c60
# https://www.xspdf.com/resolution/59308827.html
# https://github.com/tiangolo/fastapi/issues/1174
# TODO: Este link podría servir https://stackoverflow.com/questions/64497615/how-to-add-a-custom-decorator-to-a-fastapi-route
# TODO: No se que es pero tal vez sirva. https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
@search_router.post(
    '/all-branch/{client_id}', status_code=status.HTTP_200_OK, response_model=PreviewBranchOutputClient,
    summary=SearchAllBranchByClientOpenAPI.summary, responses=SearchAllBranchByClientOpenAPI.responses,
    description=SearchAllBranchByClientOpenAPI.description, response_description=SearchAllBranchByClientOpenAPI.response_description
)
async def search_locals_client(request: Request, response: Response, client_id: int, search_parameters: SearchParameters = Body(default = {})):
    logger.info('search_paramters: {}', search_parameters)

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = await validate_token(client_token=request.headers['authorization'])

    if 'error' in token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    data = await search_all_branch(search_parameters=search_parameters, client_id=client_id, client_token=request.headers['authorization'])
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
