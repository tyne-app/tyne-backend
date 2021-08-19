from fastapi import FastAPI,status,HTTPException,APIRouter, Response
from loguru import logger
from schema.local_schemas import CreateAccount
from domain.local_domain import create_account
local_router = APIRouter(
    prefix="/v1/api/local",
    tags=["Local"]
)


@local_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_account(new_account: CreateAccount):
    logger.info("new_account: {}", new_account)
    # TODO: Validar campos
    # TODO: Llamar api para crear cuenta con firebase
    # TODO: Llamar ms-backbone-locals para persisitir datos
    # TODO: Definir rollback cuando firebase y/o ms-locals no puede persisitir cuenta.
    response = create_account(new_account)

    # TODO: https: // ms - integration - apis.herokuapp.com / v1 / docs /  # /Login/post_v1_login <-- Retorna UID
    # TODO: Flujo:
    '''
    - /v1/login -> Crea usuario retorna UID
    - /v1/login -> Verifica usuario retorna JWT
    - /v1/login/validate - > Verifica JWT sesion usuario. Middleware
    - En caso de error firebase y/o ms-locales try catch -> delete firebase o delete local
    '''
    return response
