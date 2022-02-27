from typing import Optional

from pydantic import BaseModel


class ReservationResponse(BaseModel):
    reservation_id: Optional[int] = None
    payment_id: Optional[str] = None
    url_payment: Optional[str] = None
