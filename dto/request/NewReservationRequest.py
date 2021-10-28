from datetime import datetime

from pydantic import BaseModel


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
