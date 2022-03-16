from pydantic import BaseModel
from starlette import status

from src.util.ReservationStatus import ReservationStatus
from src.exception.exceptions import CustomError


class UpdateReservationRequest(BaseModel):
    payment_id: str
    status: int
    reservation_id: int

    def validate_fields(self):  # TODO: Refactorizar. Debe validar que sea un estado valido para actualizar (No necesariamente validar con todos los estados de negocio)
        if self.status != ReservationStatus.SUCCESSFUL_PAYMENT and \
                self.status != ReservationStatus.REJECTED_PAYMENT and \
                self.status != ReservationStatus.CANCELED_PAYMENT and \
                self.status != ReservationStatus.REJECTED_BY_LOCAL and \
                self.status != ReservationStatus.CONFIRMED and \
                self.status != ReservationStatus.SERVICED:
            raise CustomError(name="Validación body",
                              detail="Status debe ser 4, 5, 6, 7, 8 o 9",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Status debe ser 4, 5, 6, 7, 8 o 9")

    def is_during_payment(self) -> bool: # TODO: Validar que sea estado 5 o 6, durante el pago
        during_payment_status: list = [ReservationStatus.REJECTED_PAYMENT, ReservationStatus.CANCELED_PAYMENT]
        return self.status in during_payment_status

    def is_before_payment(self) -> bool:  # TODO: Validar que sea estado 1, 2, 3
        before_payment_status: list = [ReservationStatus.STARTED, ReservationStatus.IN_PROCESS, ReservationStatus.ERROR]
        return self.status in before_payment_status

    def is_after_payment(self) -> bool:  # TODO: Validar que sea estado 7, 8, 9
        after_payment_status: list = [ReservationStatus.CONFIRMED, ReservationStatus.SERVICED, ReservationStatus.REJECTED_BY_LOCAL]
        return self.status in after_payment_status
