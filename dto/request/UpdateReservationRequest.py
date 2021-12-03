from pydantic import BaseModel
from starlette import status

from enums.ReservationStatusEnum import ReservationStatusEnum
from exception.exceptions import CustomError


class UpdateReservationRequest(BaseModel):
    payment_id: str
    status: ReservationStatusEnum
    reservation_id: int

    def validate_fields(self):
        if self.status.value != ReservationStatusEnum.pago_exitoso.value and \
                self.status.value != ReservationStatusEnum.pago_rechazado.value and \
                self.status.value != ReservationStatusEnum.pago_cancelado.value and \
                self.status.value != ReservationStatusEnum.cancelado_local.value and \
                self.status.value != ReservationStatusEnum.reserva_confirmada.value and \
                self.status.value != ReservationStatusEnum.reserva_atendida.value:
            raise CustomError(name="Validación body",
                              detail="Status debe ser 4, 5, 6, 7, 8 o 9",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Status debe ser 4, 5, 6, 7, 8 o 9")
