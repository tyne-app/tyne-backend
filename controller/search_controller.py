from typing import Optional, Union

from fastapi import status, APIRouter, Response, Request
from loguru import logger

from configuration.openapi.search_openapi import SearchAllBranchOpenAPI, SearchAllBranchByClientOpenAPI
from schema.search_schema import PreviewBranchOutput, PreviewBranchOutputClient, BranchProfileOutput
from service.SearchService import SearchService

search_controller = APIRouter(
    prefix="/v1/locals/search",
    tags=["Search"]
)

# TODO: Crear un dto general en response para crear respuesta y retornarla, discutir con gente en qué paquete debe ir bien.
# TODO: Próxima semana se discute busqueda de locales, por sucursal o casa matriz!

# TODO: Avanzr en obtene rel perfil local perspectiva cliente por ahora.

@search_controller.get(
    '/all-branches', status_code=status.HTTP_200_OK,
    summary=SearchAllBranchOpenAPI.summary, responses=SearchAllBranchOpenAPI.responses,
    description=SearchAllBranchOpenAPI.description, response_description=SearchAllBranchOpenAPI.response_description
)  # TODO: response_model=PreviewBranchOutput
async def search_locals(
        request: Request,
        name: Optional[str] = None,
        dateReservation: Optional[str] = None,
        state: Optional[int] = None,
        sortBy: Optional[Union[int, str]] = None,
        orderBy: Optional[Union[int, str]] = None):

    # TODO: Realizar búsqueda con o sin cliente logeado
    # TODO: Si está logeado se debe extraer el ID del cliente, Para saber si tabla restaurant es favorita o no.

    logger.info('name: {}, dateReservation: {}, state: {}, sortBy: {}, orderBy: {}',
                name, dateReservation, state, sortBy, orderBy)

    search_parameters = {
        'name': name,
        'date_reservation': dateReservation,
        'state_id': state,
        'sort_by': sortBy,
        'order_by': orderBy
    }
    logger.info('search_paramters: {}', search_parameters)

    if 'authorization' in request.headers:
        # TODO: Extraer ID del token para agregarlo a query
        pass

    search_service = SearchService()
    all_branches = await search_service.search_all_branches(parameters=search_parameters)
    return all_branches

'''
@search_controller.get(
    '/all-branch/{client_id}', status_code=status.HTTP_200_OK, response_model=PreviewBranchOutputClient,
    summary=SearchAllBranchByClientOpenAPI.summary, responses=SearchAllBranchByClientOpenAPI.responses,
    description=SearchAllBranchByClientOpenAPI.description, response_description=SearchAllBranchByClientOpenAPI.response_description
)
async def search_locals_client(
    request: Request, response: Response, client_id: int,
    name: Optional[str] = None, dateReservation: Optional[str] = None,
    state: Optional[int] = None, sortBy: Optional[int] = None, orderBy: Optional[int] = None):

    logger.info('client_id: {}, name: {}, dateReservation: {}, state: {}, sortBy: {}, orderBy: {}',
                client_id, name, dateReservation, state, sortBy, orderBy)

    search_parameters = {
        'name': name,
        'date_reservation': dateReservation,
        'state_id': state,
        'sort_by': sortBy,
        'order_by': orderBy
    }

    logger.info('search_parameters: {}', search_parameters)

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = await validate_token(client_token=request.headers['authorization'])

    if 'error' in token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    data = await search_all_branch(parameters=search_parameters, client_id=client_id)
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@search_controller.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=BranchProfileOutput)
async def read_branch_profile(request: Request, response: Response, branch_id: int):  # TODO: login cliente opcional
    logger.info('branch_id: {}', branch_id)

    if 'authorization' in request.headers:
        authorization = await validate_token(client_token=request.headers['authorization'])

        if 'error' in authorization:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return authorization

    data = await search_branch_profile(branch_id=branch_id)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return data

    if type(data['data']) == list:
        return data

    if 'authorization' not in request.headers:
        data['data']['price'] = 0

    return data
'''''