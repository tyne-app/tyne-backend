from typing import Optional, Union

from fastapi import status, APIRouter, Response, Request
from fastapi.params import Depends
from loguru import logger

from configuration.database.database import SessionLocal, get_data_base
from configuration.openapi.search_openapi import SearchAllBranchOpenAPI
from dto.request.business_request_dto import NewAccount
from dto.request.business_request_dto import NewBranch
from dto.request.business_request_dto import SearchParameter
from service.JwtService import JwtService
from service.LocalService import LocalService
from service.SearchService import SearchService
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions

business_controller = APIRouter(
    prefix="/v1/business",
    tags=["Business"]
)

_throwerExceptions = ThrowerExceptions()
_localService = LocalService()
_jwt_service = JwtService()
_local_service = LocalService()
_search_service = SearchService()


async def search_parameters_params(
        page: int,
        name: Optional[str] = None,
        dateReservation: Optional[str] = None,
        stateId: Optional[int] = None,
        sortBy: Optional[Union[int, str]] = None,
        orderBy: Optional[Union[int, str]] = None):
    return {
        'page': page,
        'name': name,
        'date_reservation': dateReservation,
        'state_id': stateId,
        'sort_by': sortBy,
        'order_by': orderBy
    }


@business_controller.post("/", status_code=status.HTTP_201_CREATED)
async def register_account(new_account: NewAccount, db: SessionLocal = Depends(get_data_base)):
    return await _localService.create_new_account(new_account=new_account, db=db)


@business_controller.get('/', status_code=status.HTTP_200_OK)
async def read_account(request: Request, response: Response, db: SessionLocal = Depends(get_data_base)):
    logger.info('login')

    token_payload = await _jwt_service.verify_and_get_token_data(request)

    branch_profile = await _local_service.get_account_profile(branch_id=2, db=db)

    if branch_profile is None:
        await _throwerExceptions.throw_custom_exception(name=Constants.BRANCH_READ_ERROR,
                                                        detail=Constants.BRANCH_NOT_FOUND_ERROR_DETAIL,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return branch_profile


@business_controller.post('/branches',
                          status_code=status.HTTP_201_CREATED)
async def add_branch(request: Request, response: Response,
                     new_branch: NewBranch,
                     db: SessionLocal = Depends(get_data_base)):
    logger.info('new_branch: {}', new_branch)

    token_payload = await _jwt_service.verify_and_get_token_data(request)

    await _local_service.add_new_branch(branch_id=2, new_branch=new_branch, db=db)

    response.status_code = status.HTTP_201_CREATED
    return


@business_controller.get(
    '/branches',
    status_code=status.HTTP_200_OK,
    summary=SearchAllBranchOpenAPI.summary,
    responses=SearchAllBranchOpenAPI.responses,
    description=SearchAllBranchOpenAPI.description,
    response_description=SearchAllBranchOpenAPI.response_description
)
async def search_locals(
        request: Request,
        response: Response,
        search_parameters: SearchParameter = Depends(search_parameters_params),
        db: SessionLocal = Depends(get_data_base)):
    logger.info('search_paramters: {}', search_parameters)

    client_id = None

    if 'authorization' in request.headers:
        token_payload = await _jwt_service.verify_and_get_token_data(request)
        client_id = token_payload.id_branch_client

    return await _search_service.search_all_branches(parameters=search_parameters, client_id=client_id, db=db)


@business_controller.get('/{branch_id}', status_code=status.HTTP_200_OK)
async def read_branch_profile(request: Request,
                              response: Response,
                              branch_id: int,
                              db: SessionLocal = Depends(get_data_base)):
    logger.info('branch_id: {}', branch_id)

    client_id = None

    if 'authorization' in request.headers:
        token_payload = await _jwt_service.verify_and_get_token_data(request)
        client_id = token_payload.id_branch_client

    return await _search_service.search_branch_profile(branch_id=branch_id, client_id=client_id, db=db)
