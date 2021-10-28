from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from configuration.database import database
from dto.response.GenericResponse import create_response
from repository.dao.BankDao import get_all_banks, get_bank_by_id

bank_controller = APIRouter(
    prefix="/v1/banks",
    tags=["Banks"]
)


@bank_controller.get(
    '/',
    status_code=status.HTTP_200_OK
)
def get_banks(response: Response, db: Session = Depends(database.get_data_base)):
    data = get_all_banks(db)

    if len(data) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)


@bank_controller.get(
    '/{id}',
    status_code=status.HTTP_200_OK
)
def get_bank(response: Response, id: int, db: Session = Depends(database.get_data_base)):
    data = get_bank_by_id(id, db)

    if data is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)
