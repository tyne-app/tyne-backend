from fastapi import status, APIRouter, Response, Request
from loguru import logger
from domain.local_domain import create_account, get_branch_profile, get_branch_pre_login, add_new_branch
from schema.local_schemas import CreateAccount, Output, BranchProfilePreLoginOutput, BranchProfileLoginOutput,\
    NewBranchOutput, AddBranch
from validator.integration_validator import validate_token

local_router = APIRouter(
    prefix="/v1/locals",
    tags=["Local"]
)


@local_router.post("/register", response_model=Output, status_code=status.HTTP_201_CREATED)
async def register_account(response: Response, new_account: CreateAccount):
    logger.info("new_account: {}", new_account)
    data = await create_account(new_account)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@local_router.get('/pre-login/{email}', status_code=status.HTTP_200_OK, response_model=BranchProfilePreLoginOutput)
async def read_account_pre_login(request: Request, response: Response, email: str):
    logger.info('email: {}', email)

    data = await get_branch_pre_login(email=email)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@local_router.get('/{email}', status_code=status.HTTP_200_OK, response_model=BranchProfileLoginOutput)
async def read_account(request: Request, response: Response, email: str):
    logger.info('email: {}', email)
    #TODO: Falta probar con token validar

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    valid_token = await validate_token(client_token=request.headers['authorization'])

    if 'error' in valid_token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    data = await get_branch_profile(email=email)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@local_router.post('/new-branch', status_code=status.HTTP_201_CREATED, response_model=Ne4wBranchOutput)
async def add_branch(request: Request, response: Response, new_branch: AddBranch):
    logger.info('')

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    valid_token = await validate_token(client_token=request.headers['authorization'])

    if 'error' in valid_token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}


    # TODO: Refactorizar eliminando campo type_lega_representative, se agrega en backend.
    data = await add_new_branch(new_branch=new_branch, client_token=token)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
