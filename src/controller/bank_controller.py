from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from src.configuration.database import database
from src.repository.dao.BankDao import BankDao

bank_controller = APIRouter(
    prefix="/v1/banks",
    tags=["Banks"]
)

_bank_dao_ = BankDao()


@bank_controller.get(
    '',
    status_code=status.HTTP_200_OK
)
async def get_banks(response: Response, db: Session = Depends(database.get_data_base)):
    banks = _bank_dao_.get_banks(db)

    if len(banks) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return banks


@bank_controller.get(
    '/{id}',
    status_code=status.HTTP_200_OK
)
async def get_bank(response: Response, id: int, db: Session = Depends(database.get_data_base)):
    bank = _bank_dao_.get_bank_by_id(id, db)

    if bank is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return bank
