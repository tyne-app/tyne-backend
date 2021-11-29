from datetime import datetime

from pydantic import BaseModel
from starlette import status

from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions

_throwerExceptions = ThrowerExceptions()


class ProductRequest(BaseModel):
    id: int
    quantity: int


class NewReservationRequest(BaseModel):
    branch_id: int
    people: int
    date: datetime
    hour: str
    preference: str
    products: list[ProductRequest]

    def get_products_ids(self):
        response: list[int] = []
        for product in self.products:
            response.append(product.id)
        return response

    async def validate_fields(self):
        if self.people <= 0 or self.people > 10:
            await _throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                            detail=Constants.PEOPLE_FIELD_LEN_ERROR,
                                                            status_code=status.HTTP_400_BAD_REQUEST)
