from pydantic import BaseModel
from typing import Optional


class SearchParameters(BaseModel):
    name: Optional[str]
    date_reservation: Optional[str]
    state_id: Optional[int]
    sort_by: Optional[int]
    order_by: Optional[int]