from datetime import datetime, date

from pydantic import BaseModel
from typing import Optional
from starlette import status

from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions

_throwerExceptions = ThrowerExceptions()


class ProductRequest(BaseModel):
    id: int
    quantity: int


class NewReservationRequest(BaseModel):
    branch_id: int
    people: int
    date: datetime
    hour: str
    preference: Optional[str] = "Interior"
    products: list[ProductRequest]

    def get_products_ids(self):
        response: list[int] = []
        for product in self.products:
            response.append(product.id)
        return response
