from typing import Optional, Union

from fastapi import status, APIRouter, Response, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.configuration.database.database import get_data_base
from src.configuration.openapi.search_openapi import SearchAllBranchOpenAPI
from src.dto.request.business_request_dto import NewAccount
from src.dto.request.business_request_dto import NewBranch
from src.dto.request.business_request_dto import SearchParameter
from src.service.JwtService import JwtService
from src.service.LocalService import LocalService
from src.service.SearchService import SearchService

business_controller = APIRouter(
    prefix="/v1/business",
    tags=["Business"]
)

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
        sortBy: Optional[int] = None,
        orderBy: Optional[int] = None):
    return {
        'result_for_page': result_for_page,
        'page': page,
        'name': name,
        'date_reservation': dateReservation,
        'state_id': stateId,
        'sort_by': sortBy,
        'order_by': orderBy
    }


@business_controller.post("", status_code=status.HTTP_201_CREATED)
async def register_account(new_account: NewAccount, db: Session = Depends(get_data_base)):
    return await _localService.create_new_account(new_account=new_account, db=db)


@business_controller.get('', status_code=status.HTTP_200_OK)
async def read_account(request: Request, response: Response, db: Session = Depends(get_data_base)):
    token_payload = await _jwt_service.verify_and_get_token_data(request)

    branch_profile = await _local_service.get_account_profile(branch_id=token_payload.id_branch_client, db=db)

    if branch_profile is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return branch_profile


@business_controller.post('/branches', status_code=status.HTTP_201_CREATED)
async def add_branch(request: Request, response: Response,
                     new_branch: NewBranch,
                     db: Session = Depends(get_data_base)):
    token_payload = await _jwt_service.verify_and_get_token_data(request)
    return await _local_service.add_new_branch(branch_id=token_payload.id_branch_client, new_branch=new_branch, db=db)


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
        db: Session = Depends(get_data_base)):
    client_id = None

    if 'authorization' in request.headers:
        token_payload = await _jwt_service.verify_and_get_token_data(request)
        client_id = token_payload.id_branch_client

    restaurants = await _search_service.search_all_branches(parameters=search_parameters, client_id=client_id, db=db)

    if restaurants is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return restaurants


@business_controller.get('/{branch_id}', status_code=status.HTTP_200_OK)
async def read_branch_profile(request: Request,
                              response: Response,
                              branch_id: int,
                              db: Session = Depends(get_data_base)):
    client_id = None

    if 'authorization' in request.headers:
        token_payload = await _jwt_service.verify_and_get_token_data(request)
        client_id = token_payload.id_branch_client

    profile = await _search_service.search_branch_profile(branch_id=branch_id, client_id=client_id, db=db)

    if profile is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return profile
