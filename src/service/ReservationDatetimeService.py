import pytz
from loguru import logger
from datetime import datetime, date, timedelta
from starlette import status

from src.exception.exceptions import CustomError
from src.util.Constants import Constants
from src.util.ReservationConstant import ReservationConstant


class ReservationDatetimeService:

    @staticmethod
    def to_datetime(reservation_date: date, reservation_hour: str, tz) -> datetime:
        reservation_datetime: datetime = datetime.strptime(str(reservation_date) + ' ' + reservation_hour,
                                                           '%Y-%m-%d %H:%M').replace(tzinfo=tz)
        logger.info("reservation_datetime: {}", reservation_datetime)

        return reservation_datetime

    @staticmethod
    def is_to_future(request_datetime: datetime, reservation_datetime: datetime) -> None:
        if reservation_datetime < request_datetime:
            raise CustomError(name=Constants.RESERVATION_DATE_INVALID_ERROR,
                              detail=Constants.RESERVATION_DATETIME_DESCRIPTION_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Fecha de reserva no válida")

    @staticmethod
    def one_week_or_less(request_datetime: datetime, reservation_datetime: datetime) -> None:
        difference_as_days: int = (reservation_datetime - request_datetime).days
        logger.info("difference_as_days: {}", difference_as_days)

        if difference_as_days > ReservationConstant.WEEK_AS_DAYS:
            raise CustomError(name=Constants.RESERVATION_DATE_INVALID_ERROR,
                              detail=Constants.RESERVATION_DATE_DESCRIPTION_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Fecha de reserva no válida")

    @staticmethod
    def is_in_reservation_time_slot(opening_hour: str, closing_hour: str, request_hour: str) -> None:
        opening_hour_datetime = datetime.strptime(opening_hour, "%H:%M")
        closing_hour_datetime = datetime.strptime(closing_hour, "%H:%M")
        request_hour_datetime = datetime.strptime(request_hour, "%H:%M")

        if closing_hour_datetime < opening_hour_datetime:
            closing_hour_datetime = closing_hour_datetime + timedelta(days=1)

        logger.info("opening_hour_datetime: {}", opening_hour_datetime)
        logger.info("closing_hour_datetime: {}", closing_hour_datetime)
        logger.info("request_hour_datetime: {}", request_hour_datetime)

        difference_opening_seconds = request_hour_datetime - opening_hour_datetime

        difference_opening_hour = difference_opening_seconds.total_seconds() / ReservationConstant.HOUR_AS_SECONDS
        logger.info("difference_opening_hour: {}", difference_opening_hour)

        difference_closing_seconds = closing_hour_datetime - request_hour_datetime

        difference_closing_hour = difference_closing_seconds.total_seconds() / ReservationConstant.HOUR_AS_SECONDS
        logger.info("difference_closing_hour: {}", difference_closing_hour)

        is_valid: bool = difference_opening_hour >= ReservationConstant.TYNE_LIMIT_HOUR and \
                         difference_closing_hour >= ReservationConstant.TYNE_LIMIT_HOUR
        logger.info("is_valid: {}", is_valid)

        if not is_valid:
            raise CustomError(name=Constants.RESERVATION_TIME_INVALID_ERROR,
                              detail=Constants.RESERVATION_TIME_DESCRIPTION_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Hora de reserva debe tener diferencia de 2hrs mínimo dentro de horario de local")

    @staticmethod
    def is_valid_hour_difference(request_datetime: datetime, reservation_datetime: datetime) -> None:
        hour_difference = (reservation_datetime - request_datetime).total_seconds() / ReservationConstant.HOUR_AS_SECONDS
        logger.info("hour_difference: {}", hour_difference)

        is_valid: bool = hour_difference > ReservationConstant.TYNE_LIMIT_HOUR

        if not is_valid:
            raise CustomError(name=Constants.RESERVATION_TIME_INVALID_ERROR,
                              detail=Constants.RESERVATION_REQUEST_TIME_DESCRIPTION_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="")

    @staticmethod
    def is_in_service_hour(opening_hour: str, closing_hour: str, request_hour: str) -> bool:
        opening_datetime = datetime.strptime(opening_hour, "%H:%M")
        closing_datetime = datetime.strptime(closing_hour, "%H:%M") - timedelta(hours=2)
        request_datetime = datetime.strptime(request_hour, "%H:%M")

        logger.info("opening_datetime: {}", opening_datetime)
        logger.info("closing_datetime: {}", closing_datetime)
        logger.info("request_datetime: {}", request_datetime)

        return opening_datetime <= request_datetime <= closing_datetime

    @staticmethod
    def is_less_than_opening(opening_hour: str, request_hour: str) -> bool:
        opening_datetime = datetime.strptime(opening_hour, "%H:%M")
        request_datetime = datetime.strptime(request_hour, "%H:%M")

        return request_datetime < opening_datetime
