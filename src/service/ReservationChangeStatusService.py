from fastapi import status
from loguru import logger
from pytz import timezone
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.util.EmailSubject import EmailSubject
from src.service.EmailService import EmailService
from src.exception.exceptions import CustomError
from src.dto.request.UpdateReservationRequest import UpdateReservationRequest
from src.repository.dao.PaymentDao import PaymentDao
from src.repository.entity.PaymentEntity import PaymentEntity
from src.repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity

from src.dto.response.SimpleResponse import SimpleResponse
from src.util.TypeCoinConstant import TypeCoinConstant
from src.dto.response.UpdateReservationResponse import UpdateReservationResponse
from src.util.ReservationStatus import ReservationStatus
from src.service.KhipuService import KhipuService
from src.repository.entity.ReservationEntity import ReservationEntity
from src.service.ReservationEventService import ReservationEventService
from src.repository.dao.UserDao import UserDao
from src.util.Constants import Constants
from src.util.ReservationConstant import ReservationConstant
from src.repository.entity.BranchScheduleEntity import BranchScheduleEntity
from src.repository.dao.ReservationProductDao import ReservationProductDao
from src.repository.dao.BranchDao import BranchDao
from src.repository.dao.ReservationDao import ReservationDao


class ReservationChangeStatusService:
    _payment_dao_ = PaymentDao()
    _email_service = EmailService()
    _khipu_service = KhipuService()
    _country_time_zone = timezone('Chile/Continental')
    _reservation_event_service = ReservationEventService()
    _use_dao = UserDao()
    _reservation_product_dao = ReservationProductDao()
    _branch_dao = BranchDao()
    _reservation_dao_ = ReservationDao()

    def rejected_or_canceled_reservation_payment(self, reservation_id: int, reservation_status: int):
        self._reservation_dao_.add_reservation_status(status=reservation_status,
                                                      reservation_id=reservation_id)

        return SimpleResponse("Reserva actualizada correctamente a estado confirmado")

    def successful_reservation_payment(self, reservation: ReservationEntity,
                                       reservation_updated: UpdateReservationRequest,
                                       request_datetime: datetime, client_email: str,
                                       branch_email: str, db: Session):

        payment = self._payment_dao_.get_payment(reservation_id=reservation_updated.reservation_id, db=db)

        if payment:
            raise CustomError(name="Ya existe un pago asociado",
                              detail="Error",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Ya existe un pago asociado")

        payment_khipu = self._khipu_service.verify_payment(reservation_updated.payment_id)
        logger.info("payment_khipu: {}", payment_khipu)

        payment = PaymentEntity()
        payment.date = datetime.now(self._country_time_zone)
        payment.method = "Khipu"
        payment.amount = payment_khipu.amount
        payment.type_coin_id = TypeCoinConstant.CLP
        payment.receipt_url = payment_khipu.receipt_url
        payment.reservation_id = reservation_updated.reservation_id

        payment_response = self._payment_dao_.create_payment(payment=payment, db=db)

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.SUCCESSFUL_PAYMENT,
                                                      reservation_id=reservation_updated.reservation_id)

        response = UpdateReservationResponse()
        response.payment_id = payment_response.id
        response.amount = payment_response.amount
        response.reservation_id = payment_response.reservation_id
        response.receipt_url = payment_response.receipt_url
        logger.info("response: {}", response.__dict__)

        data: dict = self._get_reservation_data_to_email(reservation=reservation, db=db)

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.SUCCESSFUL_PAYMENT,
                                       receiver_email=client_email, data=data)

        job_id: str = str(reservation_updated.reservation_id)
        kwargs: dict = {
            'job_id': job_id,
            'branch_email': branch_email,
            'client_email': client_email
        }
        logger.info("kwargs: {}", kwargs)

        if request_datetime.date() == reservation.reservation_date:
            logger.info("Reservation is today")
            self._reservation_event_service.create_job(func=self._reservation_event_service.create_reservation_event,
                                                       difference_as_seconds=1, kwargs=kwargs)
            return response

        nearest_branch_opening_datetime: datetime = self.get_available_datetime(request_datetime=request_datetime,
                                                                                branch_id=reservation.branch_id, db=db)

        difference_as_seconds: int = round((nearest_branch_opening_datetime - request_datetime).total_seconds())
        logger.info("Difference as seconds: {}", difference_as_seconds)

        self._reservation_event_service.create_job(func=self._reservation_event_service.create_reservation_event,
                                                   difference_as_seconds=difference_as_seconds, kwargs=kwargs)
        return response

    def rejected_reservation_by_local(self, reservation_id: int, client_email: str):
        # TODO: Las cancelaciones de rembolso sin rembolso, etc, se maneja por backend según el datetime de la cancelacion
        # TODO: Falta obtener la razón del por qué se rechaza.

        job_id: str = str(reservation_id)
        logger.info("job_id: {}", job_id)

        self._reservation_event_service.delete_job(job_id=job_id)

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.CANCELLATION_BY_LOCAL,
                                       receiver_email=client_email)

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.REJECTED_BY_LOCAL,
                                                      reservation_id=reservation_id)

        return SimpleResponse("Reserva actualizada correctamente a estado rechazado por local")

    def confirmed_reservation(self, reservation: ReservationEntity, request_datetime: datetime, client_email: str, branch_email: str, db: Session):
        logger.info("Confirmed reservation has been started")

        job_id: str = str(reservation.id)
        self._reservation_event_service.delete_job(job_id=job_id)

        data: dict = self._get_reservation_data_to_email(reservation=reservation, db=db)
        logger.info("Data to email: {}", data)

        if request_datetime.date() == reservation.reservation_date:
            self._email_service.send_email(user=Constants.USER, subject=EmailSubject.CONFIRMATION_TO_CLIENT,
                                           receiver_email=client_email, data=data)
            return SimpleResponse("Reserva actualizada correctamente a estado confirmado")

        reservation_day: int = reservation.reservation_date.isoweekday() - ReservationConstant.DAY_ADJUSTMENT
        branch_schedule_entity = self._branch_dao.get_day_schedule(branch_id=reservation.branch_id,
                                                                   day=reservation_day, db=db)

        branch_opening_datetime: datetime = datetime \
            .strptime(str(reservation.reservation_date) + ' ' +
                      branch_schedule_entity.opening_hour, '%Y-%m-%d %H:%M').astimezone(self._country_time_zone)
        logger.info("Branch opening datetime: {}", branch_opening_datetime)

        kwargs: dict = {
            'job_id': job_id,
            'branch_email': branch_email,
            'client_email': client_email
        }
        logger.info("kwargs: {}", kwargs)

        difference_as_seconds: int = round((branch_opening_datetime - request_datetime).total_seconds())

        self._reservation_event_service.create_job(func=self._reservation_event_service.reminder_email,
                                                   difference_as_seconds=difference_as_seconds, kwargs=kwargs)

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.CONFIRMED, reservation_id=reservation.id)

        return SimpleResponse("Reserva actualizada correctamente a estado confirmado")

    def serviced_reservation(self, reservation_id: int):
        self._reservation_dao_.add_reservation_status(status=ReservationStatus.SERVICED, reservation_id=reservation_id)
        return SimpleResponse("Reserva actualizada correctamente a estado servico")

    def _get_reservation_data_to_email(self, reservation: ReservationEntity, db: Session) -> dict:
        products: list = self._reservation_product_dao.get_al_products_by_reservation(reservation_id=reservation.id, db=db)
        name: str = self._branch_dao.get_name(branch_id=reservation.branch_id, db=db)

        data: dict = {
            'name': name,
            'date': reservation.reservation_date,
            'hour': reservation.hour,
            'total_amount': reservation.amount + reservation.tyne_commission,
            'products': products
            }

        logger.info("data: {}", data)

        return data

    def get_available_datetime(self, request_datetime: datetime, branch_id: int, db: Session) -> datetime:

        day: int = 1

        while day <= ReservationConstant.WEEK_AS_DAYS:
            next_datetime = request_datetime + timedelta(days=day)
            logger.info("next datetime: {}", next_datetime)

            next_day = next_datetime.isoweekday() - ReservationConstant.DAY_ADJUSTMENT
            branch_schedule: BranchScheduleEntity = self._branch_dao.get_day_schedule(branch_id=branch_id,
                                                                                      day=next_day, db=db)
            if branch_schedule:
                nearest_branch_opening_datetime: datetime = datetime\
                    .strptime(str(next_datetime.date()) + ' ' + str(branch_schedule.opening_hour), '%Y-%m-%d %H:%M')\
                    .astimezone(self._country_time_zone)
                logger.info("nearest_branch_opening_datetime: {}", nearest_branch_opening_datetime)
                return nearest_branch_opening_datetime

            day += 1

        raise CustomError(name="No existe día disponible",
                          detail="No existe día dentro de una semana para avisar a local",
                          status_code=status.HTTP_400_BAD_REQUEST,
                          cause="No existe día")
