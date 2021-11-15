from pydantic import BaseModel
from starlette import status
from exception.exceptions import CustomError
from validator.SharedValidator import SharedValidator
import datetime


class LocalReservationRequest:
    reservation_date: datetime
    result_for_page: int
    page_number: int
    status_reservation: int

    @classmethod
    def validate_fields(cls, local_reservation_request):

        if not local_reservation_request.reservation_date:
            raise CustomError(name="Validación body",
                              detail="Fecha de reserva no puede estar vacia",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Fecha de reserva no puede estar vacia")

        if local_reservation_request.page_number < 1:
            raise CustomError(name="Validación body",
                              detail="N° de página debe ser mayor a 0",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="N° de  página debe ser mayor a 0")

        if local_reservation_request.result_for_page < 1:
            raise CustomError(name="Validación body",
                              detail="Resultado por página debe ser mayor a 0",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Resultado por página debe ser mayor a 0")

        if local_reservation_request.status_reservation < 0:
            raise CustomError(name="Validación body",
                              detail="Estado de la reserva debe ser mayor a 0",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Estado de la reserva debe ser mayor a 0")

