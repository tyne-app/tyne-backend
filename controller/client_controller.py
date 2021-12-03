from fastapi import status, APIRouter, Response, Depends, Request
from sqlalchemy.orm import Session

from configuration.database import database
from dto.request.ClientRequestDTO import ClientRequestDTO
from dto.request.ClientSocialRegistrationRequest import ClientSocialRegistrationRequest
from service.ClientService import ClientService
from service.JwtService import JwtService
from service.ReservationService import ReservationService

client_controller = APIRouter(
    prefix="/v1/clients",
    tags=["Clients"]
)

_client_service_ = ClientService()
_jwt_service_ = JwtService()
_reservation_service_ = ReservationService()


@client_controller.get('/reservations', status_code=status.HTTP_200_OK)
async def get_client_reservations(request: Request, db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request)
    return await _reservation_service_.get_reservations(client_id=token_payload.id_branch_client, db=db)


@client_controller.get(
    '/{id}',
    status_code=status.HTTP_200_OK
)
async def get_user_by_id(response: Response, id: int, db: Session = Depends(database.get_data_base)):
    return await _client_service_.get_client_by_id(client_id=id, db=db)


@client_controller.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
async def create_client(response: Response, client_req: ClientRequestDTO,
                        db: Session = Depends(database.get_data_base)):
    return await _client_service_.create_client(client_req, db)


@client_controller.post(
    '/social-networks',
    status_code=status.HTTP_201_CREATED
)
async def create_client_with_social_networks(response: Response, client: ClientSocialRegistrationRequest,
                                             db: Session = Depends(database.get_data_base)):
    return await _client_service_.create_client_social_networks(client, db)
