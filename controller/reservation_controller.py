from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from configuration.database import database
from dto.request.NewReservationRequest import NewReservationRequest
from exception.exceptions import CustomError
from service import menu_service
from loguru import logger

reservation_controller = APIRouter(
    prefix="/v1/reservations",
    tags=["Reservations"]
)


@reservation_controller.post('/', status_code=status.HTTP_201_CREATED)
async def create_reservation(response: Response,
                             reservation_request: NewReservationRequest,
                             db: Session = Depends(database.get_data_base)):
    pass
