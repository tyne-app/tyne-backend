from typing import Optional, Union

from fastapi import status, APIRouter, Response, Request
from fastapi.params import Depends
from loguru import logger
from configuration.database.database import SessionLocal, get_data_base
from configuration.openapi.search_openapi import SearchAllBranchOpenAPI
from dto.request.search_request_dto import SearchParameter
from dto.response.search_response_dto import ListBranchOutput, BranchProfileOutput
from service.LocalService import LocalService
from dto.request.local_request_dto import NewAccount, NewBranch
from service.JwtService import JwtService
from service.SearchService import SearchService

business_controller = APIRouter(
    prefix="/v1/business",
    tags=["Business"]
)


# TODO: Avanzr en obtene rel perfil local perspectiva cliente por ahora.

async def search_parameters_params(
        name: Optional[str] = None,
        dateReservation: Optional[str] = None,
        stateId: Optional[int] = None,
        sortBy: Optional[Union[int, str]] = None,
        orderBy: Optional[Union[int, str]] = None):
    return {
        'name': name,
        'date_reservation': dateReservation,
        'state_id': stateId,
        'sort_by': sortBy,
        'order_by': orderBy
    }


@business_controller.post("/", status_code=status.HTTP_201_CREATED)
async def register_account(new_account: NewAccount, db: SessionLocal = Depends(get_data_base)):
    logger.info("new_account: {}", new_account)
    local_service = LocalService()
    account_created = await local_service.create_new_account(new_account=new_account, db=db)

    return account_created


@business_controller.get('/', status_code=status.HTTP_200_OK)  # TODO: response_model=BranchProfileLoginOutput
async def read_account(request: Request, response: Response, db: SessionLocal = Depends(get_data_base)):
    logger.info('login')

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    jwt_service = JwtService()
    token_payload = jwt_service.verify_and_get_token_data(token=token)

    local_service = LocalService()
    branch_profile = local_service.get_account_profile(branch_id=token_payload.id_branch_client, db=db)

    if branch_profile['data'] is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return branch_profile


@business_controller.post('/branchs', status_code=status.HTTP_201_CREATED)  # TODO: response_model=NewBranchOutput
async def add_branch(request: Request, response: Response,
                     new_branch: NewBranch, db: SessionLocal = Depends(get_data_base)):
    logger.info('new_branch: {}', new_branch)

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']

    jwt_service = JwtService()
    token_payload = jwt_service.verify_and_get_token_data(token=token)

    local_service = LocalService()
    branch_profile = await local_service.add_new_branch(branch_id=token_payload.id_branch_client, new_branch=new_branch,
                                                        db=db)
    return branch_profile


@business_controller.get(
    '/branches', status_code=status.HTTP_200_OK,
    response_model=ListBranchOutput,
    summary=SearchAllBranchOpenAPI.summary, responses=SearchAllBranchOpenAPI.responses,
    description=SearchAllBranchOpenAPI.description, response_description=SearchAllBranchOpenAPI.response_description
)
async def search_locals(
        request: Request,
        response: Response,
        search_parameters: SearchParameter = Depends(search_parameters_params),
        db: SessionLocal = Depends(get_data_base)):
    logger.info('search_paramters: {}', search_parameters)

    client_id = None
    if 'authorization' in request.headers:
        token = request.headers['authorization']
        jwt_service = JwtService()
        token_payload = jwt_service.verify_and_get_token_data(token=token)
        client_id = token_payload.id_branch_client

    search_service = SearchService()
    all_branches = await search_service \
        .search_all_branches(parameters=search_parameters, client_id=client_id, db=db)

    if all_branches['data'] is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return all_branches


@business_controller.get('/{branch_id}', status_code=status.HTTP_200_OK, response_model=BranchProfileOutput)
async def read_branch_profile(request: Request,
                              response: Response,
                              branch_id: int,
                              db: SessionLocal = Depends(get_data_base)):
    logger.info('branch_id: {}', branch_id)

    client_id = None
    if 'authorization' in request.headers:
        token = request.headers['authorization']
        jwt_service = JwtService()
        token_payload = jwt_service.verify_and_get_token_data(token=token)
        client_id = token_payload.id_branch_client

    search_service = SearchService()
    branch_profile = await search_service.search_branch_profile(branch_id=branch_id, client_id=client_id, db=db)

    if branch_profile is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    return branch_profile
