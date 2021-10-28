from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from configuration.database import database
from service.ClientService import ClientService

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
