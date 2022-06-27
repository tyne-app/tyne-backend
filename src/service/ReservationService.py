import uuid
from zoneinfo import ZoneInfo
import pytz
import locale
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from src.configuration.Settings import Settings
from src.dto.request.ClientCancelReservationRequest import ClientCancelReservationRequest
from src.dto.request.LocalReservationsRequest import LocalReservationRequest
from src.dto.request.NewReservationRequest import NewReservationRequest
from src.dto.request.UpdateReservationRequest import UpdateReservationRequest
from src.dto.response.LocalReservationsResponse import LocalReservationsResponse
from src.dto.response.ReservationDetailResponse import ReservationDetailResponse
from src.dto.response.ReservationResponse import ReservationResponse
from src.exception.exceptions import CustomError
from src.repository.dao.BranchDao import BranchDao
from src.repository.dao.ClientDao import ClientDao
from src.repository.dao.PaymentDao import PaymentDao
from src.repository.dao.ProductDao import ProductDao
from src.repository.dao.ReservationDao import ReservationDao
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.ReservationEntity import ReservationEntity
from src.repository.entity.ReservationProductEntity import ReservationProductEntity
from src.repository.entity.ProductEntity import ProductEntity
from src.repository.dao.ReservationProductDao import ReservationProductDao
from src.repository.dao.UserDao import UserDao
from src.service.MercadoPagoService import MercadoPagoService
from src.service.EmailService import EmailService
from src.util.Constants import Constants
from src.util.ReservationConstant import ReservationConstant
from src.util.ReservationStatus import ReservationStatus
from src.util.EmailSubject import EmailSubject
from src.service.ReservationEventService import ReservationEventService
from src.service.ReservationChangeStatusService import ReservationChangeStatusService
from src.service.ReservationDatetimeService import ReservationDatetimeService


class ReservationService:
    _client_dao_ = ClientDao()
    _mercado_pago_service = MercadoPagoService()
    _product_dao_ = ProductDao()
    _reservation_dao_ = ReservationDao()
    _payment_dao_ = PaymentDao()
    _user_dao_ = UserDao()
    _reservation_product_dao = ReservationProductDao()
    _email_service = EmailService()
    _branch_dao = BranchDao()
    _chile_tz = pytz.timezone('Chile/Continental')
    _reservation_event_service = ReservationEventService()
    _reservation_change_status_service = ReservationChangeStatusService()
    _local_currency = locale.setlocale(locale.LC_ALL, '')  # TODO: Dar formato moneda chilena

    async def create_reservation(self, client_id: int, new_reservation: NewReservationRequest, db: Session):
        logger.info("new_reservation: {}", dict(new_reservation))
        # TODO: Validar campos de new_reservation por regla de negocio. Validar cantidad de personas en la reserva
        #  ¿Qué pasa si en el intervalo de tiempo de confirmación reserva el local cierra la sucursal o el día de la reserva?

        client: ClientEntity = self._client_dao_.get_client_by_id(client_id=client_id, db=db)

        reservation_count: int = self._reservation_dao_. \
            get_reservation_count_by_date(branch_id=new_reservation.branch_id,
                                          date_reservation=new_reservation.date, db=db)
        logger.info("reservation_count: {}", reservation_count)

        if reservation_count >= ReservationConstant.MAX_RESERVATION:
            raise CustomError(name=Constants.BRANCH_MAX_RESERVATION,
                              detail=Constants.CLIENT_UNAUTHORIZED,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause=f"Sucursal ya cuenta con el máximo de reservas para el día")

        reservation_day: int = new_reservation.date.isoweekday() - ReservationConstant.DAY_ADJUSTMENT
        logger.info("reservation_day: {}", reservation_day)

        branch_schedule_entity = self._branch_dao.get_day_schedule(branch_id=new_reservation.branch_id,
                                                                   day=reservation_day, db=db)
        logger.info("branch_schedule_entity: {}", branch_schedule_entity)

        if not branch_schedule_entity:
            raise CustomError(name=Constants.BRANCH_DAY_UNABLE,
                              detail=Constants.BRANCH_DAY_UNABLE_DETAIL,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Sucursal no disponible para el día requerido")

        request_datetime: datetime = datetime.now(tz=self._chile_tz)
        logger.info("request_datetime: {}", request_datetime)

        reservation_datetime: datetime = ReservationDatetimeService \
            .to_datetime(reservation_date=new_reservation.date.date(),
                         reservation_hour=new_reservation.hour,
                         tz=self._chile_tz)

        ReservationDatetimeService.is_to_future(request_datetime=request_datetime,
                                                reservation_datetime=reservation_datetime)

        ReservationDatetimeService.one_week_or_less(request_datetime=request_datetime,
                                                    reservation_datetime=reservation_datetime)

        ReservationDatetimeService.is_in_reservation_time_slot(opening_hour=branch_schedule_entity.opening_hour,
                                                               closing_hour=branch_schedule_entity.closing_hour,
                                                               request_hour=new_reservation.hour)

        ReservationDatetimeService.is_valid_hour_difference(request_datetime=request_datetime,
                                                            reservation_datetime=reservation_datetime)

        products = self._product_dao_.get_products_by_ids(products_id=new_reservation.get_products_ids(),
                                                          branch_id=new_reservation.branch_id, db=db)

        if not products or len(new_reservation.products) != len(products):
            raise CustomError(name=Constants.PRODUCT_NOT_EXIST,
                              detail=Constants.PRODUCT_NOT_EXIST,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="No existe(n) producto(s) para la reserva")

        reservation_products: list[ReservationProductEntity] = []
        product_list: list = new_reservation.products
        product_dict: dict = {product_list[i].id: product_list[i].quantity for i in range(len(product_list))}
        logger.info("product_dict: {}", product_dict)

        amount: int = 0
        for product in products:
            quantity = product_dict[product.id]
            amount += product.amount * quantity
            reservation_product = self._create_reservation_product(product=product, quantity=quantity)
            reservation_products.append(reservation_product)

        logger.info("amount: {}", amount)

        if Settings.ENVIRONMENT == "Production":
            if amount < ReservationConstant.MIN_AMOUNT:
                raise CustomError(name=Constants.BUY_INVALID_ERROR,
                                  detail=f"La compra debe ser mínimo de ${ReservationConstant.MIN_AMOUNT}",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause=Constants.BUY_INVALID_ERROR)

        fifteen_percent: int = round(amount * ReservationConstant.TYNE_COMMISSION)
        logger.info("15% amount: {}", fifteen_percent)

        total_amount: int = amount + fifteen_percent
        logger.info("Tota amount: {}", total_amount)

        reservation_entity: ReservationEntity = self._create_reservation_entity(new_reservation=new_reservation,
                                                                                client_id=client_id, amount=amount,
                                                                                fifteen_percent=fifteen_percent)
        logger.info("reservation_entity: {}", reservation_entity.__dict__)

        reservation_id = self._reservation_dao_.create_reservation(reservation=reservation_entity,
                                                                   products=reservation_products,
                                                                   db=db)

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.STARTED,
                                                      reservation_id=reservation_id)

        response_mercado_pago = self._mercado_pago_service.create_link(amount=total_amount,
                                                                       payer_email=client.user.email,
                                                                       transaction_id=reservation_entity.transaction_id)
        logger.info("response_mercado_pago: {}", response_mercado_pago)

        if response_mercado_pago.status != status.HTTP_201_CREATED:
            self._reservation_dao_.add_reservation_status(status=ReservationStatus.ERROR,
                                                          reservation_id=reservation_id)

            raise CustomError(name=Constants.MP_GET_ERROR,
                              detail=Constants.MP_GET_ERROR,
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="Error obtener datos mercado pago")

        self._reservation_dao_.update_payment_id_reservation(reservation_id=reservation_id,
                                                             payment_id=response_mercado_pago.payment_id,
                                                             db=db)
        logger.info("Se actualiza id de pago")

        self._reservation_dao_.add_reservation_status(status=ReservationStatus.IN_PROCESS,
                                                      reservation_id=reservation_id)

        response = ReservationResponse()
        response.url_payment = response_mercado_pago.url
        response.reservation_id = reservation_id
        response.payment_id = response_mercado_pago.payment_id
        logger.info("reservation response: {}", response.__dict__)

        return response

    def _create_reservation_product(self, product: ProductEntity,
                                    quantity: int) -> ReservationProductEntity:  # TODO: Se podría moder metodo a otro lado
        reservation_product = ReservationProductEntity()
        reservation_product.name_product = product.name
        reservation_product.category_product = product.category.name
        reservation_product.amount = product.amount
        reservation_product.quantity = quantity
        reservation_product.description = product.description
        return reservation_product

    def _create_reservation_entity(self, new_reservation: NewReservationRequest,
                                   client_id: int, amount: int,
                                   fifteen_percent: int) -> ReservationEntity:  # TODO: Se podría moder metodo a otro lado
        reservation_entity: ReservationEntity = ReservationEntity()
        reservation_entity.reservation_date = new_reservation.date
        reservation_entity.preference = new_reservation.preference
        reservation_entity.client_id = client_id
        reservation_entity.branch_id = new_reservation.branch_id
        reservation_entity.people = new_reservation.people
        reservation_entity.hour = new_reservation.hour
        reservation_entity.transaction_id = str(uuid.uuid4())
        reservation_entity.amount = amount
        reservation_entity.tyne_commission = fifteen_percent
        return reservation_entity

    async def local_reservations(self,
                                 branch_id: int,
                                 reservation_date: datetime,
                                 result_for_page: int,
                                 page_number: int,
                                 status_reservation: int, db):

        local_reservation_request = LocalReservationRequest()
        local_reservation_request.reservation_date = reservation_date
        local_reservation_request.result_for_page = result_for_page
        local_reservation_request.page_number = page_number
        local_reservation_request.status_reservation = status_reservation

        await local_reservation_request.validate_fields(local_reservation_request)

        reservations = self._reservation_dao_.local_reservations(db,
                                                                 branch_id,
                                                                 reservation_date,
                                                                 status_reservation)

        reservations_date = self._reservation_dao_.local_reservations_date(db,
                                                                           branch_id,
                                                                           status_reservation,
                                                                           reservation_date,
                                                                           result_for_page,
                                                                           page_number)

        local_reservations_response = LocalReservationsResponse()
        response = local_reservations_response.local_reservations(reservations,
                                                                  reservations_date,
                                                                  result_for_page,
                                                                  page_number)
        return response

    async def reservation_detail(self, reservation_id: int, db) -> ReservationDetailResponse:
        logger.info("reservation_id: {}", reservation_id)

        reservations: list = self._reservation_dao_.reservation_detail(reservation_id=reservation_id, db=db)
        logger.info("reservations: {}", reservations)

        reservation_detail: ReservationDetailResponse = ReservationDetailResponse()
        logger.info("reservation_detail: {}", reservation_detail)

        return reservation_detail.reservation_detail(reservations)

    async def get_pending_reservations(self, client_id: int, db: Session) -> list:
        reservations = self._reservation_dao_.get_reservations(client_id, db)

        first_done = False
        reservation_id = 0
        pending_reservation = []
        for x in reservations:
            if reservation_id != x.id:
                first_done = False

            if not first_done:
                if x.status_id == ReservationStatus.SUCCESSFUL_PAYMENT or x.status_id == ReservationStatus.CONFIRMED:
                    pending_reservation.append(x)

            reservation_id = x.id
            first_done = True
        return pending_reservation

    async def update_reservation(self, reservation_updated: UpdateReservationRequest,
                                 db: Session):

        logger.info("reservation_updated: {}", reservation_updated.__dict__)
        reservation_updated.validate_fields()

        reservation: ReservationEntity = self._reservation_dao_ \
            .get_reservation(reservation_id=reservation_updated.reservation_id,
                             payment_id=reservation_updated.payment_id, db=db)

        if not reservation:
            raise CustomError(name="Reserva no existe",
                              detail="Reserva no existe",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Reserva no existe")

        last_reservation_status: int = self._reservation_dao_.get_last_reservation_status(reservation_id=reservation.id,
                                                                                          db=db)
        logger.info("last_reservation_status: {}", last_reservation_status)
        logger.info("reservation_updated: {}", reservation_updated)

        client_email: str = self._user_dao_.get_email_by_cient(client_id=reservation.client_id, db=db)
        logger.info("client_email: {}", client_email)

        branch_email: str = self._user_dao_.get_email_by_branch(branch_id=reservation.branch_id, db=db)
        logger.info("branch_email: {}", branch_email)

        match reservation_updated.status:
            case ReservationStatus.STARTED | ReservationStatus.IN_PROCESS | \
                 ReservationStatus.ERROR | ReservationStatus.NO_CONFIRMED:
                self._raise_reservation_status_error()

            case ReservationStatus.REJECTED_PAYMENT:
                if last_reservation_status != ReservationStatus.IN_PROCESS:
                    self._raise_reservation_status_error()

                return self._reservation_change_status_service \
                    .rejected_reservation_payment(reservation_id=reservation_updated.reservation_id,
                                                  reservation_status=last_reservation_status)

            case ReservationStatus.CANCELED_PAYMENT:
                if last_reservation_status != ReservationStatus.IN_PROCESS:
                    self._raise_reservation_status_error()

                return self._reservation_change_status_service \
                    .canceled_reservation_payment(reservation=reservation, reservation_status=last_reservation_status,
                                                  branch_email=branch_email, db=db)

            case ReservationStatus.SUCCESSFUL_PAYMENT:
                if last_reservation_status != ReservationStatus.IN_PROCESS:
                    self._raise_reservation_status_error()

                return self._reservation_change_status_service \
                    .successful_reservation_payment(reservation=reservation, reservation_updated=reservation_updated,
                                                    client_email=client_email, branch_email=branch_email, db=db)

            case ReservationStatus.REJECTED_BY_LOCAL:
                # TODO: Obtener razón del por qué se rechaza
                if last_reservation_status == ReservationStatus.CONFIRMED or last_reservation_status == ReservationStatus.SUCCESSFUL_PAYMENT:
                    return self._reservation_change_status_service \
                        .rejected_reservation_by_local(reservation=reservation, client_email=client_email, db=db)
                else:
                    self._raise_reservation_status_error()

            case ReservationStatus.CONFIRMED:
                if last_reservation_status != ReservationStatus.SUCCESSFUL_PAYMENT:
                    self._raise_reservation_status_error()

                return self._reservation_change_status_service \
                    .confirmed_reservation(reservation=reservation, client_email=client_email,
                                           branch_email=branch_email, db=db)
            case _:
                self._raise_reservation_status_error()

    async def client_cancel_reservation(self, cancelation: ClientCancelReservationRequest, id_client: int, db: Session):
        reservation: ReservationEntity = self._reservation_dao_.get_reservation_by_client(cancelation.reservation_id,
                                                                                          id_client,
                                                                                          db)
        if not reservation:
            raise CustomError(name="Reserva no existe",
                              detail="Reserva no existe",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Reserva no existe")

        last_reservation_status = self._reservation_dao_.get_last_reservation_status(cancelation.reservation_id, db)

        if last_reservation_status == ReservationStatus.SUCCESSFUL_PAYMENT \
                or last_reservation_status == ReservationStatus.CONFIRMED:

            reservation_datetime = datetime.combine(reservation.reservation_date,
                                                    datetime.min.strptime(reservation.hour, '%H:%M').time())
            reservation_datetime = reservation_datetime.replace(tzinfo=ZoneInfo('Chile/Continental'))

            logger.info("reservation datetime: " + str(reservation_datetime))
            logger.info("datetime now........: " + str(datetime.now(self._country_time_zone)))

            minutes_diff = (reservation_datetime - datetime.now(self._country_time_zone)).total_seconds() / 60
            logger.info("minutes diff........: " + str(minutes_diff))

            if minutes_diff < 120:
                raise CustomError(
                    name="Solo se puede cancelar la reserva como máximo 2 horas antes de la hora comprometida.",
                    detail="Ya no es posible cancelar la reserva",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    cause="Ya no es posible cancelar la reserva")

            payment = self._payment_dao_.get_payment(reservation_id=cancelation.reservation_id, db=db)
            self._mercado_pago_service.refund_payment(payment.payment_mp_id)

            self._reservation_dao_.add_reservation_status(ReservationStatus.CLIENT_REJECT_RESERVATION,
                                                          cancelation.reservation_id)

            job_id: str = str(cancelation.reservation_id)
            logger.info("job_id: {}", job_id)
            self._reservation_event_service.delete_job(job_id=job_id)

            # send email to client
            data: dict = self._reservation_change_status_service.get_reservation_data_to_email(reservation, db=db)
            client_email = self._user_dao_.get_email_by_cient(client_id=reservation.client_id, db=db)
            self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.REFUND_CANCELLATION,
                                           receiver_email=client_email, data=data)

            # send email to branch manager
            branch_email = self._user_dao_.get_email_by_branch(branch_id=reservation.branch_id, db=db)
            data_email_to_branch: dict = self._reservation_change_status_service.get_reservation_data_to_email(
                reservation=reservation, db=db)
            self._email_service.send_email(user=Constants.BRANCH, subject=EmailSubject.REFUND_CANCELLATION_TO_BRANCH,
                                           receiver_email=branch_email, data=data_email_to_branch)
        else:
            raise CustomError(name="No es posible cancelar la reserva.",
                              detail="No es posible cancelar la reserva",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="No es posible cancelar la reserva")

        return True

    def _raise_reservation_status_error(self):
        raise CustomError(name="Error con estado de reserva",
                          detail="Estado de reserva no es válido para actualizar",
                          status_code=status.HTTP_400_BAD_REQUEST,
                          cause="Estado de reserva no es válido para actualizar")
