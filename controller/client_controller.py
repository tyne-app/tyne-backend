from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from configuration.database import database
from dto.request.ClientRequestDTO import ClientRequestDTO
from exception.exceptions import CustomError
from service.ClientService import ClientService
from loguru import logger
client_controller = APIRouter(
    prefix="/v1/clients",
    tags=["Clients"]
)

_client_service_ = ClientService()


@client_controller.get(
    '/{id}',
    status_code=status.HTTP_200_OK
)
def get_user_by_id(response: Response, id: int, db: Session = Depends(database.get_data_base)):
    client = _client_service_.get_client_by_id(client_id=id, db=db)

    if client is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return client


@client_controller.post(
    '/',
    status_code=status.HTTP_200_OK
)
def create_client(response: Response, client_req: ClientRequestDTO, db: Session = Depends(database.get_data_base)):
    try:
        return _client_service_.create_client(client_req, db)

    except CustomError as error:
        logger.error(error.detail)
        raise CustomError(name=error.name,
                          detail=error.detail,
                          status_code=error.status_code,
                          cause=error.cause)

    except Exception as error:
        logger.error(error)
        raise CustomError(name="Error create_client",
                          detail="Error al crear cliente",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          cause=error.__cause__)

