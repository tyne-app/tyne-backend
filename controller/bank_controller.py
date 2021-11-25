from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session

from configuration.database import database
from repository.dao.BankDao import get_all_banks, get_bank_by_id
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions

bank_controller = APIRouter(
    prefix="/v1/banks",
    tags=["Banks"]
)

_throwerExceptions = ThrowerExceptions()


@bank_controller.get(
    '/',
    status_code=status.HTTP_200_OK
)
async def get_banks(response: Response, db: Session = Depends(database.get_data_base)):
    data = get_all_banks(db)

    if len(data) == 0:
        await _throwerExceptions.throw_custom_exception(name=Constants.BANK_READ_ERROR,
                                                        detail=Constants.BANK_READ_ERROR_DETAIL,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return data


@bank_controller.get(
    '/{id}',
    status_code=status.HTTP_200_OK
)
async def get_bank(response: Response, id: int, db: Session = Depends(database.get_data_base)):
    data = get_bank_by_id(id, db)

    if data is None:
        await _throwerExceptions.throw_custom_exception(name=Constants.BANK_READ_ERROR,
                                                        detail=Constants.BANK_READ_ERROR_DETAIL,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return data
