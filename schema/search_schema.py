from pydantic import BaseModel
from typing import Optional


class SearchParameters(BaseModel):
    name: str
    date_reservation: str
    state_id: int
    sort_by: int
    order_by: int