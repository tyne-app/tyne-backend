import datetime

from starlette import status

from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions

_throwerExceptions = ThrowerExceptions()


class LocalReservationRequest:
    reservation_date: datetime
    result_for_page: int
    page_number: int
    status_reservation: int

    @classmethod
    async def validate_fields(cls, local_reservation_request):

        if not local_reservation_request.reservation_date:
            await _throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                            detail=Constants.DATE_EMPTY_ERROR,
                                                            status_code=status.HTTP_400_BAD_REQUEST)

        if local_reservation_request.page_number < 1:
            await _throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                            detail=Constants.PAGE_LEN_ERROR,
                                                            status_code=status.HTTP_400_BAD_REQUEST)

        if local_reservation_request.result_for_page < 1:
            await _throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                            detail=Constants.RESULT_PAGE_LEN_ERROR,
                                                            status_code=status.HTTP_400_BAD_REQUEST)

        if local_reservation_request.status_reservation < 0:
            await _throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                            detail=Constants.STATUS_RESERVATION_LEN_ERROR,
                                                            status_code=status.HTTP_400_BAD_REQUEST)
