from pydantic import BaseModel
from starlette import status

from src.util.ReservationStatus import ReservationStatus
from src.exception.exceptions import CustomError


class UpdateReservationRequest(BaseModel):
    payment_id: str
    status: int
    reservation_id: int

    def validate_fields(self):
        if self.status.value != ReservationStatus.SUCCESSFUL_PAYMENT and \
                self.status.value != ReservationStatus.REJECTED_PAYMENT and \
                self.status.value != ReservationStatus.CANCELED_PAYMENT and \
                self.status.value != ReservationStatus.REJECTED_BY_LOCAL and \
                self.status.value != ReservationStatus.CONFIRMED and \
                self.status.value != ReservationStatus.SERVICED:
            raise CustomError(name="Validación body",
                              detail="Status debe ser 4, 5, 6, 7, 8 o 9",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Status debe ser 4, 5, 6, 7, 8 o 9")
