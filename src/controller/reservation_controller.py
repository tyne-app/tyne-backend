from datetime import datetime

from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from src.configuration.database import database
from src.dto.request.NewReservationRequest import NewReservationRequest
from src.dto.request.UpdateReservationRequest import UpdateReservationRequest
from src.dto.response.ReservationResponse import ReservationResponse
from src.service.JwtService import JwtService
from src.service.ReservationService import ReservationService
from threading import Thread
from time import sleep
# TODO: Verify
reservation_controller = APIRouter(
    prefix="/v1/reservations",
    tags=["Reservations"]
)

_jwt_service_ = JwtService()
_reservation_service_ = ReservationService()
# TODO: Eiminar endopoint
@reservation_controller.get('/check/{reservation_id}', status_code=status.HTTP_200_OK)
async def check(reservation_id: str):
    return _reservation_service_.check_thread(thread_name=reservation_id)
# TODO: Eiminar endopoint
@reservation_controller.post('/{reservation_id}', status_code=status.HTTP_200_OK)
async def test_path(reservation_id: int):
    print("Reservation time dict")
    print(_reservation_service_._reservation_timer)
    print("Largo diccionario: %s", len(_reservation_service_._reservation_timer))
    return _reservation_service_.crear(reservation_id=reservation_id)


@reservation_controller.post('', status_code=status.HTTP_200_OK, response_model=ReservationResponse)
async def create_reservation(request: Request,
                             new_reservation_request: NewReservationRequest,
                             db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request=request)
    return await _reservation_service_.create_reservation(client_id=token_payload.id_branch_client,
                                                          new_reservation=new_reservation_request,
                                                          db=db)


@reservation_controller.put('', status_code=status.HTTP_200_OK)
async def update_reservation(request: Request,
                             reservation_updated: UpdateReservationRequest,
                             db: Session = Depends(database.get_data_base)):
    await _jwt_service_.verify_and_get_token_data(request=request)
    return await _reservation_service_.update_reservation(reservation_updated, db=db)


@reservation_controller.get('/{id}', status_code=status.HTTP_200_OK)
async def reservation_detail(request: Request, id: int,
                             db: Session = Depends(database.get_data_base)):
    await _jwt_service_.verify_and_get_token_data(request=request)
    return await _reservation_service_.reservation_detail(reservation_id=id, db=db)


@reservation_controller.get('',
                            status_code=status.HTTP_200_OK)
async def local_reservations(request: Request,
                             reservation_date: datetime,
                             status_reservation: int,
                             result_for_page: int,
                             page_number: int,
                             db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request=request)
    return await _reservation_service_.local_reservations(branch_id=token_payload.id_branch_client,
                                                          reservation_date=reservation_date,
                                                          result_for_page=result_for_page,
                                                          page_number=page_number,
                                                          status_reservation=status_reservation,
                                                          db=db)
