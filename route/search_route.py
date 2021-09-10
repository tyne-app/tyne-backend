from typing import Optional, Union

from fastapi import status, APIRouter, Response, Request
from loguru import logger

from domain.search_domain import search_all_branch, search_branch_profile
from openapi.search_openapi import SearchAllBranchByClientOpenAPI, SearchAllBranchOpenAPI
from schema.search_schema import PreviewBranchOutput, PreviewBranchOutputClient, BranchProfileOutput
from validator.integration_validator import validate_token

search_router = APIRouter(
    prefix="/v1/api/search",
    tags=["Search"]
)


@search_router.get(
    '/all-branch', status_code=status.HTTP_200_OK, response_model=PreviewBranchOutput,
    summary=SearchAllBranchOpenAPI.summary, responses=SearchAllBranchOpenAPI.responses,
    description=SearchAllBranchOpenAPI.description, response_description=SearchAllBranchOpenAPI.response_description
)
async def search_locals(
        response: Response,
        name: Optional[str] = None, dateReservation: Optional[str] = None,
        state: Optional[int] = None, sortBy: Optional[Union[int, str]] = None, orderBy: Optional[Union[int, str]] = None):

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

    data = await search_all_branch(parameters=search_parameters)
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@search_router.get(
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


@search_router.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=BranchProfileOutput)
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
