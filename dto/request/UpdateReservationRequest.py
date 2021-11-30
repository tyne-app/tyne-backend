from pydantic import BaseModel

from enums.ReservationStatusEnum import ReservationStatusEnum


class UpdateReservationRequest(BaseModel):
    payment_id: str
    status: ReservationStatusEnum
    reservation_id: int
