from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.orm import Session
from configuration.database import database
from dto.request.NewReservationRequest import NewReservationRequest

from service.JwtService import JwtService
from service.ReservationService import ReservationService

reservation_controller = APIRouter(
    prefix="/v1/reservations",
    tags=["Reservations"]
)

_jwt_service_ = JwtService()
_service_ = ReservationService()


@reservation_controller.post('/', status_code=status.HTTP_201_CREATED)
async def create_reservation(request: Request,
                             response: Response,
                             reservation_request: NewReservationRequest,
                             db: Session = Depends(database.get_data_base)):
    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    token_payload = _jwt_service_.verify_and_get_token_data(token=token)

    _service_.create_reservation(client_id=token_payload.id_branch_client, reservation=reservation_request, db=db)
