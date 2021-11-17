from fastapi import APIRouter, Depends, Response, status, Request
from loguru import logger
from sqlalchemy.orm import Session
from configuration.database import database
from dto.request.NewReservationRequest import NewReservationRequest
from dto.response.ReservationResponse import ReservationResponse
from exception.exceptions import CustomError
from service.JwtService import JwtService
from service.ReservationService import ReservationService
from datetime import datetime

reservation_controller = APIRouter(
    prefix="/v1/reservations",
    tags=["Reservations"]
)

_jwt_service_ = JwtService()
_service_ = ReservationService()


@reservation_controller.get('/{id}', status_code=status.HTTP_200_OK)
async def reservation_detail(request: Request, response: Response, id: int,
                             db: Session = Depends(database.get_data_base)):
    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    token_payload = _jwt_service_.verify_and_get_token_data(token=token)
    response_detail = _service_.reservation_detail(reservation_id=id, db=db)

    return response_detail


@reservation_controller.get('/',
                            status_code=status.HTTP_200_OK)
def local_reservations(request: Request,
                       response: Response,
                       reservation_date: datetime,
                       status_reservation: int,
                       result_for_page: int,
                       page_number: int,
                       db: Session = Depends(database.get_data_base)):
    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    token_payload = _jwt_service_.verify_and_get_token_data(token=token)
    return ReservationService.local_reservations(branch_id=token_payload.id_branch_client,
                                                 reservation_date=reservation_date,
                                                 result_for_page=result_for_page,
                                                 page_number=page_number,
                                                 status_reservation=status_reservation,
                                                 db=db)


@reservation_controller.post('/', status_code=status.HTTP_200_OK, response_model=ReservationResponse)
async def create_reservation(request: Request,
                             response: Response,
                             reservation_request: NewReservationRequest,
                             db: Session = Depends(database.get_data_base)):
    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    token_payload = _jwt_service_.verify_and_get_token_data(token=token)

    response = _service_.create_reservation(client_id=token_payload.id_branch_client, reservation=reservation_request,
                                            db=db)
    return response



