from pydantic import BaseModel
from starlette import status
from src.exception.exceptions import CustomError


class ClientCancelReservationRequest(BaseModel):
    reservation_id: int

    def validate_fields(self):
        if not self.reservation_id:
            raise CustomError(name="Reservation id es inválido",
                              detail="Reservation id es inválido",
                              status_code=status.HTTP_400_BAD_REQUEST)
