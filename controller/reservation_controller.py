from fastapi import APIRouter, Depends, Response, status, Request
from sqlalchemy.orm import Session
from auth.AuthValidator import AuthValidator
from configuration.database import database
from dto.request.NewReservationRequest import NewReservationRequest
from dto.request.UpdateReservationRequest import UpdateReservationRequest
from dto.response.ReservationResponse import ReservationResponse
from service.JwtService import JwtService
from service.ReservationService import ReservationService
from datetime import datetime

reservation_controller = APIRouter(
    prefix="/v1/reservations",
    tags=["Reservations"]
)

_jwt_service_ = JwtService()
_reservation_service_ = ReservationService()
_auth_validator_ = AuthValidator()


@reservation_controller.post('/', status_code=status.HTTP_200_OK, response_model=ReservationResponse)
def create_reservation(request: Request,
                       reservation_request: NewReservationRequest,
                       db: Session = Depends(database.get_data_base)):
    token_payload = _auth_validator_.validate_token(request=request)

    response = _reservation_service_.create_reservation(client_id=token_payload.id_branch_client,
                                                        reservation=reservation_request,
                                                        db=db)
    return response


@reservation_controller.put('/', status_code=status.HTTP_200_OK)
def update_reservation(request: Request,
                       reservation_updated: UpdateReservationRequest,
                       db: Session = Depends(database.get_data_base)):
    token_payload = _auth_validator_.validate_token(request=request)

    response = _reservation_service_.update_reservation(reservation_updated, db=db)
    return response


@reservation_controller.get('/{id}', status_code=status.HTTP_200_OK)
def reservation_detail(request: Request, id: int,
                       db: Session = Depends(database.get_data_base)):
    token_payload = _auth_validator_.validate_token(request=request)
    response_detail = _reservation_service_.reservation_detail(reservation_id=id, db=db)

    return response_detail


@reservation_controller.get('/',
                            status_code=status.HTTP_200_OK)
def local_reservations(request: Request,
                       reservation_date: datetime,
                       status_reservation: int,
                       result_for_page: int,
                       page_number: int,
                       db: Session = Depends(database.get_data_base)):
    token_payload = _auth_validator_.validate_token(request=request)

    return _reservation_service_.local_reservations(branch_id=token_payload.id_branch_client,
                                                    reservation_date=reservation_date,
                                                    result_for_page=result_for_page,
                                                    page_number=page_number,
                                                    status_reservation=status_reservation,
                                                    db=db)
