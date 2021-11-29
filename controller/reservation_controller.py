from datetime import datetime

from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.orm import Session

from configuration.database import database
from dto.request.NewReservationRequest import NewReservationRequest
from dto.response.ReservationResponse import ReservationResponse
from service.JwtService import JwtService
from service.ReservationService import ReservationService

reservation_controller = APIRouter(
    prefix="/v1/reservations",
    tags=["Reservations"]
)

_jwt_service_ = JwtService()
_service_ = ReservationService()


@reservation_controller.get('/{id}', status_code=status.HTTP_200_OK)
async def reservation_detail(request: Request, response: Response, id: int,
                             db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request)
    response_detail = await _service_.reservation_detail(reservation_id=id, db=db)

    return response_detail


@reservation_controller.get('/',
                            status_code=status.HTTP_200_OK)
async def local_reservations(request: Request,
                             response: Response,
                             reservation_date: datetime,
                             status_reservation: int,
                             result_for_page: int,
                             page_number: int,
                             db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request)
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
    token_payload = await _jwt_service_.verify_and_get_token_data(request)
    return _service_.create_reservation(client_id=63,
                                        reservation=reservation_request,
                                        db=db)
