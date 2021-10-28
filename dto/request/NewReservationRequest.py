from datetime import datetime

from pydantic import BaseModel
from starlette import status

from exception.exceptions import CustomError


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

    def validate_fields(self):
        if self.people <= 0 or self.people > 10:
            raise CustomError(name="Campo people debe ser mayor a 0 y menor a 11",
                              detail="Validación",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Campo people debe ser mayor a 0 y menor a 11")