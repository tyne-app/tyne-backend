from typing import Optional, Union

from fastapi import status, APIRouter, Response, Request
from fastapi.params import Depends
from loguru import logger

from configuration.database.database import SessionLocal, get_data_base
from configuration.openapi.search_openapi import SearchAllBranchOpenAPI
from dto.request.business_request_dto import SearchParameter
from dto.response.business_response_dto import ListBranchOutput
from dto.response.business_response_dto import BranchProfileOutput
from dto.response.business_response_dto import RegisterAccountOutput
from service.LocalService import LocalService
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
        result_for_page: int,
        page: int,
        name: Optional[str] = None,
        dateReservation: Optional[str] = None,
        stateId: Optional[int] = None,
        sortBy: Optional[Union[int, str]] = None,
        orderBy: Optional[Union[int, str]] = None):
    return {
        'result_for_page': result_for_page,
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
    await _jwt_service.verify_and_get_token_data(request)

    branch_profile = await _local_service.get_account_profile(branch_id=2, db=db)

    if branch_profile is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return branch_profile


@business_controller.post('/branches', status_code=status.HTTP_201_CREATED)
async def add_branch(request: Request, response: Response,
                     new_branch: NewBranch,
                     db: SessionLocal = Depends(get_data_base)):
    token_payload = await _jwt_service.verify_and_get_token_data(request)
    await _local_service.add_new_branch(branch_id=token_payload.id_branch_client, new_branch=new_branch, db=db)

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
    token_payload = await _jwt_service.verify_and_get_token_data(request)

    restaurants = await _search_service.search_all_branches(parameters=search_parameters,
                                                            client_id=token_payload.id_branch_client, db=db)

    if restaurants is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return restaurants


@business_controller.get('/{branch_id}', status_code=status.HTTP_200_OK)
async def read_branch_profile(request: Request,
                              response: Response,
                              branch_id: int,
                              db: SessionLocal = Depends(get_data_base)):
    token_payload = await _jwt_service.verify_and_get_token_data(request)

    profile = await _search_service.search_branch_profile(branch_id=branch_id, client_id=token_payload.id_branch_client,
                                                          db=db)

    if profile is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return profile
