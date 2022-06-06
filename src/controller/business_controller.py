from typing import Optional, Union

from fastapi import status, APIRouter, Response, Request, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.configuration.database.database import get_data_base
from src.configuration.openapi.search_openapi import SearchAllBranchOpenAPI
from src.dto.request.DeleteBranchImageRequest import DeleteBranchImageRequest
from src.dto.request.NewBranchScheduleDto import NewBranchScheduleDto
from src.dto.request.business_request_dto import NewAccount
from src.dto.request.business_request_dto import NewBranch
from src.dto.request.business_request_dto import SearchParameter
from src.dto.response.SimpleResponse import SimpleResponse
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.service.JwtService import JwtService
from src.service.LocalService import LocalService
from src.service.SearchService import SearchService
from src.util.Constants import Constants
from src.util.UserType import UserType
from loguru import logger

business_controller = APIRouter(
    prefix="/v1/business",
    tags=["Business"]
)

_localService = LocalService()
_jwt_service = JwtService()
_local_service = LocalService()
_search_service = SearchService()
_throwerExceptions = ThrowerExceptions()


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

    if token_payload.rol != UserType.MANAGER:
        logger.error("User type is client, the request is UNAUTHORIZED")
        await _throwerExceptions.throw_custom_exception(name=Constants.TOKEN_INVALID_ERROR,
                                                        detail=Constants.TOKEN_INVALID_ERROR,
                                                        status_code=status.HTTP_401_UNAUTHORIZED)

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


@business_controller.put('/schedule', status_code=status.HTTP_201_CREATED)
async def update_branch_schedule(request: Request,
                                 response: Response,
                                 schedule: NewBranchScheduleDto,
                                 db: Session = Depends(get_data_base)):
    await _jwt_service.verify_and_get_token_data(request)
    await _local_service.update_branch_schedule(schedule, db=db)
    response.status_code = status.HTTP_201_CREATED
    return SimpleResponse("Horario actualizado correctamente")


@business_controller.get('/{branch_id}/images', status_code=status.HTTP_200_OK)
async def get_images(request: Request,
                     response: Response,
                     branch_id: int,
                     db: Session = Depends(get_data_base)):
    await _jwt_service.verify_and_get_token_data(request)

    images = await _local_service.get_images(branch_id=branch_id, db=db)

    if images is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return images


@business_controller.post(
    '/{branch_id}/images',
    status_code=status.HTTP_200_OK
)
async def upload_image(request: Request,
                       response: Response,
                       image: UploadFile = File(...),
                       db: Session = Depends(get_data_base)):
    token_payload = await _jwt_service.verify_and_get_token_data(request)
    response = await _local_service.upload_image(token_payload.id_branch_client, image, db)
    return response


@business_controller.delete(
    '/{branch_id}/images',
    status_code=status.HTTP_200_OK
)
async def delete_image(request: Request,
                       response: Response,
                       branch_id: int,
                       deleteBranchImage: DeleteBranchImageRequest,
                       db: Session = Depends(get_data_base)):
    token_payload = await _jwt_service.verify_and_get_token_data(request)
    response = await _local_service.delete_image(token_payload.id_branch_client, deleteBranchImage, db)
    return response
