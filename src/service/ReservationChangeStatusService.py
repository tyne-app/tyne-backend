from fastapi import status
from loguru import logger
from pytz import timezone
from datetime import datetime, timedelta, date

from sqlalchemy.orm import Session

from src.util.EmailSubject import EmailSubject
from src.service.EmailService import EmailService
from src.exception.exceptions import CustomError
from src.dto.request.UpdateReservationRequest import UpdateReservationRequest
from src.repository.dao.PaymentDao import PaymentDao
from src.repository.entity.PaymentEntity import PaymentEntity

from src.dto.response.SimpleResponse import SimpleResponse
from src.util.TypeCoinConstant import TypeCoinConstant
from src.dto.response.UpdateReservationResponse import UpdateReservationResponse
from src.util.ReservationStatus import ReservationStatus
from src.service.MercadoPagoService import MercadoPagoService
from src.repository.entity.ReservationEntity import ReservationEntity
from src.service.ReservationEventService import ReservationEventService
from src.service.ReservationDatetimeService import ReservationDatetimeService
from src.repository.dao.UserDao import UserDao
from src.util.Constants import Constants
from src.util.ReservationConstant import ReservationConstant
from src.repository.entity.BranchScheduleEntity import BranchScheduleEntity
from src.repository.dao.ReservationProductDao import ReservationProductDao
from src.repository.dao.BranchDao import BranchDao
from src.repository.dao.ReservationDao import ReservationDao
from src.repository.dao.ClientDao import ClientDao
from src.configuration.Settings import Settings


class ReservationChangeStatusService:
    _payment_dao_ = PaymentDao()
    _email_service = EmailService()
    _mercado_pago_service = MercadoPagoService()
    _chile_tz = timezone('Chile/Continental')
    _reservation_event_service = ReservationEventService()
    _use_dao = UserDao()
    _reservation_product_dao = ReservationProductDao()
    _branch_dao = BranchDao()
    _reservation_dao_ = ReservationDao()
    _client_dao = ClientDao()
    _settings_ = Settings()
    _NEXT_DAY: int = 1

    def rejected_reservation_payment(self, reservation_id: int, reservation_status: int):
        self._reservation_dao_.add_reservation_status(status=reservation_status,
                                                      reservation_id=reservation_id)

        return SimpleResponse("Reserva actualizada correctamente a estado pago rechazado")

    def canceled_reservation_payment(self, reservation: ReservationEntity, reservation_status: int, branch_email: str,
                                     db: Session):

        data: dict = self.get_reservation_data_to_email(reservation=reservation, db=db)

        self._email_service.send_email(user=Constants.BRANCH, subject=EmailSubject.CANCELLATION_BY_CLIENT,
                                       receiver_email=branch_email, data=data)

        self._reservation_dao_.add_reservation_status(status=reservation_status,
                                                      reservation_id=reservation.id)

        return SimpleResponse("Reserva actualizada correctamente a estado cancelado")

    def successful_reservation_payment(self, reservation: ReservationEntity,
                                       reservation_updated: UpdateReservationRequest,
                                       client_email: str, branch_email: str, db: Session):

        payment = self._payment_dao_.get_payment(reservation_id=reservation_updated.reservation_id, db=db)
        logger.info("payment: {}", payment)
        if payment:
            raise CustomError(name="Ya existe un pago asociado",
                              detail="Error",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Ya existe un pago asociado")

        request_datetime: datetime = datetime.now(tz=self._chile_tz)
        logger.info("request datetime: {}", request_datetime)

        self._validate_request_date(request_date=request_datetime.date(),
                                    reservation_date=reservation.reservation_date)

        payment_mp = self._mercado_pago_service.verify_payment(reservation_updated.payment_number)
        logger.info("payment_mercadopago: {}", payment_mp)

        payment = PaymentEntity()
        payment.date = datetime.now(self._chile_tz)
        payment.method = "Mercado Pago"
        payment.amount = payment_mp.get("transaction_amount")
        payment.type_coin_id = TypeCoinConstant.CLP
        payment.receipt_url = "https://api.mercadopago.com/v1/payments/" + reservation_updated.payment_number + "?access_token=" + self._settings_.MP_ACCESS_TOKEN
        payment.reservation_id = reservation_updated.reservation_id
        payment.payment_mp_id = reservation_updated.payment_number

        payment_response = self._payment_dao_.create_payment(payment=payment, db=db)

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.SUCCESSFUL_PAYMENT,
                                                      reservation_id=reservation_updated.reservation_id)

        response = UpdateReservationResponse()
        response.payment_id = payment_response.id
        response.amount = payment_response.amount
        response.reservation_id = payment_response.reservation_id
        response.receipt_url = payment_response.receipt_url
        logger.info("response: {}", response.__dict__)

        data: dict = self.get_reservation_data_to_email(reservation=reservation, db=db)
        data['reservation_id'] = reservation.id

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.SUCCESSFUL_PAYMENT,
                                       receiver_email=client_email)

        job_id: str = str(reservation_updated.reservation_id)
        kwargs: dict = {
            'job_id': job_id,
            'branch_email': branch_email,
            'client_email': client_email,
            'payment_mp_id': payment_response.payment_mp_id,
            'data': data
        }
        logger.info("kwargs: {}", kwargs)

        available_datetime: datetime = self._get_available_datetime(request_datetime=request_datetime,
                                                                    reservation=reservation, db=db)
        logger.info("Run date to execute reservation job: {}", available_datetime)

        self._reservation_event_service.create_job(func=self._reservation_event_service.create_reservation_event,
                                                   run_date=available_datetime, kwargs=kwargs)

        return response

    def rejected_reservation_by_local(self, reservation: ReservationEntity, client_email: str, db: Session):
        # TODO: Las cancelaciones de rembolso sin rembolso, etc, se maneja por backend según el datetime de la cancelacion
        # TODO: Falta obtener la razón del por qué se rechaza.
        request_datetime: datetime = datetime.now(self._chile_tz)
        logger.info("request datetime: {}", request_datetime)

        self._validate_request_date(request_date=request_datetime.date(),
                                    reservation_date=reservation.reservation_date)

        job_id: str = str(reservation.id)
        logger.info("job_id: {}", job_id)

        payment = self._payment_dao_.get_payment(reservation_id=reservation.id, db=db)

        self._mercado_pago_service.refund_payment(payment.payment_mp_id)

        self._reservation_event_service.delete_job(job_id=job_id)

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.CANCELLATION_BY_LOCAL,
                                       receiver_email=client_email)

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.REJECTED_BY_LOCAL,
                                                      reservation_id=reservation.id)

        return SimpleResponse("Reserva actualizada correctamente a estado rechazado por local")

    def confirmed_reservation(self, reservation: ReservationEntity, client_email: str, branch_email: str, db: Session):
        logger.info("Confirmed reservation has been started")

        request_datetime: datetime = datetime.now()
        logger.info("request datetime: {}", request_datetime)

        self._validate_request_date(request_date=request_datetime.date(),
                                    reservation_date=reservation.reservation_date)
        job_id: str = str(reservation.id)
        self._reservation_event_service.delete_job(job_id=job_id)

        data: dict = self.get_reservation_data_to_email(reservation=reservation, db=db)
        logger.info("Data to email: {}", data)

        if request_datetime.date() == reservation.reservation_date:
            self._reservation_dao_.add_reservation_status(status=ReservationStatus.CONFIRMED,
                                                          reservation_id=reservation.id)

            self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.CONFIRMATION_TO_CLIENT,
                                           receiver_email=client_email, data=data)
            return SimpleResponse("Reserva actualizada correctamente a estado confirmado")

        reservation_day: int = reservation.reservation_date.isoweekday() - ReservationConstant.DAY_ADJUSTMENT
        branch_schedule_entity = self._branch_dao.get_day_schedule(branch_id=reservation.branch_id,
                                                                   day=reservation_day, db=db)

        branch_opening_datetime: datetime = ReservationDatetimeService. \
            to_datetime(reservation_date=reservation.reservation_date,
                        reservation_hour=branch_schedule_entity.opening_hour,
                        tz=self._chile_tz)

        logger.info("Branch opening datetime: {}", branch_opening_datetime)

        kwargs: dict = {
            'job_id': job_id,
            'branch_email': branch_email,
            'client_email': client_email,
            'data': data
        }
        logger.info("kwargs: {}", kwargs)

        self._reservation_event_service.create_job(func=self._reservation_event_service.reminder_email,
                                                   run_date=branch_opening_datetime, kwargs=kwargs)

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.CONFIRMED, reservation_id=reservation.id)

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.CONFIRMATION_TO_CLIENT,
                                       receiver_email=client_email, data=data)

        return SimpleResponse("Reserva actualizada correctamente a estado confirmado")

    def get_reservation_data_to_email(self, reservation: ReservationEntity, db: Session) -> dict:
        products: list = self._reservation_product_dao.get_all_products_by_reservation(reservation_id=reservation.id,
                                                                                       db=db)

        branch_name: str = self._branch_dao.get_name(branch_id=reservation.branch_id, db=db)
        client_name: str = self._client_dao.get_client_name(client_id=reservation.client_id, db=db)

        data: dict = {
            'branch_name': branch_name,
            'client_name': client_name,
            'date': reservation.reservation_date.strftime("%d-%m-%Y"),
            'hour': reservation.hour,
            'total_amount': reservation.amount + reservation.tyne_commission,
            'products': products,
            'reservation_id': reservation.id
        }

        logger.info("data: {}", data)

        return data

    def _get_available_datetime(self, request_datetime: datetime, reservation: ReservationEntity,
                                db: Session) -> datetime:

        day: int = request_datetime.isoweekday() - ReservationConstant.DAY_ADJUSTMENT
        branch_schedule: BranchScheduleEntity = self._branch_dao.get_day_schedule(branch_id=reservation.branch_id,
                                                                                  day=day, db=db)

        if branch_schedule:
            request_hour = str(request_datetime.time())[0:5]
            logger.info("request_hour: {}", request_hour)
            # TODO: Verificar que pasa si se reserva a las 3:00hrs para mismo día a las 17:00hrs.
            # TODO: Parece que no envia email el mismo día, sino el día siguiente.
            # TODO: Se debe hacer:
            # TODO: ¿Es inferior al horario de apertura? Sí, entonces enviar correo en horario de apertura.
            # TODO: Caso contrario se prosigue con la lógica ya creada.
            is_valid: bool = ReservationDatetimeService.is_in_service_hour(opening_hour=branch_schedule.opening_hour,
                                                                           closing_hour=branch_schedule.closing_hour,
                                                                           request_hour=request_hour)
            if is_valid:
                available_datetime: datetime = request_datetime + timedelta(seconds=30)
                logger.info("available_datetime: {}", available_datetime)
                return available_datetime

        return self._get_nearest_available_opening(request_datetime=request_datetime, branch_id=reservation.branch_id, db=db)

    def _get_nearest_available_opening(self, request_datetime: datetime, branch_id: int, db: Session) -> datetime:

        day: int = self._NEXT_DAY
        next_datetime = request_datetime + timedelta(days=self._NEXT_DAY)

        while day <= ReservationConstant.WEEK_AS_DAYS:

            logger.info("next datetime: {}", next_datetime)

            next_day = next_datetime.isoweekday() - ReservationConstant.DAY_ADJUSTMENT
            branch_schedule: BranchScheduleEntity = self._branch_dao.get_day_schedule(branch_id=branch_id,
                                                                                      day=next_day, db=db)
            if branch_schedule:
                return ReservationDatetimeService.\
                    to_datetime(reservation_date=next_datetime.date(), reservation_hour=branch_schedule.opening_hour, tz=self._chile_tz)

            next_datetime = request_datetime + timedelta(days=day)
            day += self._NEXT_DAY

        raise CustomError(name="No existe día disponible",
                          detail="No existe día dentro de una semana para avisar a local",
                          status_code=status.HTTP_400_BAD_REQUEST,
                          cause="No existe día")

    def _validate_request_date(self, request_date: date, reservation_date: date) -> None:
        logger.info("Validate request date has been started")

        if request_date > reservation_date:
            raise CustomError(name="Error con fecha de petición reserva",
                              detail="No puede ser fecha de reserva menor a fecha petición reserva",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="No puede ser fecha de reserva menor a fecha petición reserva")
