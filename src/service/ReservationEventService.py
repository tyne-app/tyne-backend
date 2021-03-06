from loguru import logger
from src.util.Constants import Constants
from src.util.EmailSubject import EmailSubject
from src.util.ReservationStatus import ReservationStatus
from src.repository.dao.ReservationDao import ReservationDao
from src.service.EmailService import EmailService
from src.service.MercadoPagoService import MercadoPagoService
from src.configuration.database.database import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from datetime import datetime, timedelta


class ReservationEventService:

    _email_service = EmailService()
    _scheduler: BackgroundScheduler = scheduler
    _reservation_dao_ = ReservationDao()
    _mercado_pago_service = MercadoPagoService()

    def create_job(self, func, run_date: datetime, **kwargs):
        logger.info("func: {}, run_date: {}, kwargs: {}", func, run_date, kwargs)
        kwargs = kwargs.get('kwargs')
        kwargs['run_date']: datetime = run_date

        self._scheduler.add_job(func=func, id=kwargs.get('job_id'), misfire_grace_time=5, coalesce=True,
                                replace_existing=True, trigger='date', run_date=run_date, kwargs=kwargs)
        logger.info("Job reservation event created")

    def delete_job(self, job_id: str):
        logger.info("job id: {}", job_id)

        try:
            self._scheduler.pause_job(job_id)
            logger.info("Job id has been paused: {} ", job_id)

            self._scheduler.remove_job(job_id)
            logger.info("Job id has been deleted: {}", job_id)
        except JobLookupError as e:
            logger.error("Job reservation event not found: {}", e)

    def create_reservation_event(self, **kwargs):

        logger.info("Reservation event has started. It will send an email to confirm/cancel by branch")
        logger.info("kwargs: {}", kwargs)

        self._email_service.send_email(user=Constants.BRANCH, subject=EmailSubject.CONFIRMATION_TO_LOCAL,
                                       receiver_email=kwargs.get('branch_email'), data=kwargs.get('data'))

        run_date: datetime = kwargs.get('run_date') + timedelta(minutes=60)
        logger.info("Run date to cancel reservation: {}", run_date)

        self._scheduler.add_job(func=self.cancel_reservation, kwargs=kwargs,
                                id=kwargs.get('job_id'), misfire_grace_time=5, coalesce=True,
                                replace_existing=True, trigger='date', run_date=run_date)

        logger.info("Reservation event has updated to 60 minutes. At the end, reservation will be cancelled")

    def cancel_reservation(self, **kwargs):
        logger.info("Cancellation reservation event has started")
        logger.info("kwargs: {}", kwargs)

        data: dict = kwargs.get('data')
        payment_mp_id: str = kwargs.get('payment_mp_id')

        self._mercado_pago_service.refund_payment(payment_mp_id)

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.LOCAL_NO_CONFIRMATION_TO_CLIENT,
                                       receiver_email=kwargs.get('client_email'), data=data)

        self._email_service.send_email(user=Constants.BRANCH, subject=EmailSubject.LOCAL_NO_CONFIRMATION_TO_LOCAL,
                                       receiver_email=kwargs.get('branch_email'), data=data)

        reservation_id: int = int(kwargs.get('job_id'))

        self._reservation_dao_. add_reservation_status(status=ReservationStatus.NO_CONFIRMED,
                                                       reservation_id=reservation_id)

    def reminder_email(self, **kwargs):
        logger.info("kwargs: {}", kwargs)
        data: dict = kwargs.get('data')

        self.delete_job(job_id=kwargs.get('job_id'))

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.REMINDER_TO_CLIENT,
                                       receiver_email=kwargs.get('client_email'), data=data)
        self._email_service.send_email(user=Constants.BRANCH, subject=EmailSubject.REMINDER_TO_LOCAL,
                                       receiver_email=kwargs.get('branch_email'), data=data)
