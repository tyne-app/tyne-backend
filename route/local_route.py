from fastapi import FastAPI,status,HTTPException,APIRouter, Response
from loguru import logger
from schema.local_schemas import CreateAccount, Output
from domain.local_domain import create_account
local_router = APIRouter(
    prefix="/v1/api/local",
    tags=["Local"]
)


@local_router.post("/register", response_model=Output, status_code=status.HTTP_201_CREATED)
async def register_account(response: Response, new_account: CreateAccount):
    logger.info("new_account: {}", new_account)
    # TODO: Validar campos
    # TODO: Llamar api para crear cuenta con firebase
    # TODO: Llamar ms-backbone-locals para persisitir datos
    # TODO: Definir rollback cuando firebase y/o ms-locals no puede persisitir cuenta.
    data = await create_account(new_account)

    # TODO: https: // ms - integration - apis.herokuapp.com / v1 / docs /  # /Login/post_v1_login <-- Retorna UID
    # TODO: Flujo:
    # TODO: Enviar correo a local crear cuenta al siguiente endpoint
    # https://backbone-email.herokuapp.com/v1/docs/#/Email/post_v1_emails_welcome_local
    '''
    la request te pide estos dos campos {
        "url": "string", Este lo devuelve el servicio de registro, lo devuelve firebase para vlaidar usuario despues
        "email": "string" Email del cliente
        }
    
    
    
    - /v1/login -> Crea usuario retorna UID
    - /v1/login -> Verifica usuario retorna JWT
    - /v1/login/validate - > Verifica JWT sesion usuario. Middleware
    - En caso de error firebase y/o ms-locales try catch -> delete firebase o delete local
    '''
    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
