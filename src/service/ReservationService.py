import uuid
from datetime import timezone, datetime
from loguru import logger
from sqlalchemy.orm import Session
from starlette import status
from src.dto.request.LocalReservationsRequest import LocalReservationRequest
from src.dto.request.NewReservationRequest import NewReservationRequest
from src.dto.request.UpdateReservationRequest import UpdateReservationRequest
from src.dto.response.LocalReservationsResponse import LocalReservationsResponse
from src.dto.response.ReservationDetailResponse import ReservationDetailResponse
from src.dto.response.ReservationResponse import ReservationResponse
from src.dto.response.SimpleResponse import SimpleResponse
from src.dto.response.UpdateReservationResponse import UpdateReservationResponse
from src.util.ReservationStatus import ReservationStatus
from src.exception.exceptions import CustomError
from src.repository.dao.BranchDao import BranchDao
from src.repository.dao.ClientDao import ClientDao
from src.repository.dao.PaymentDao import PaymentDao
from src.repository.dao.ProductDao import ProductDao
from src.repository.dao.ReservationDao import ReservationDao
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.PaymentEntity import PaymentEntity
from src.repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from src.repository.entity.ReservationEntity import ReservationEntity
from src.repository.entity.ReservationProductEntity import ReservationProductEntity
from src.repository.entity.ProductEntity import ProductEntity
from src.service.KhipuService import KhipuService
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.service.EmailService import EmailService
from src.util.EmailSubject import EmailSubject
from src.repository.dao.UserDao import UserDao
from src.configuration.database.database import scheduler
from apscheduler.schedulers.background import BackgroundScheduler



class ReservationService:
    _client_dao_ = ClientDao()
    _khipu_service = KhipuService()
    _product_dao_ = ProductDao()
    _reservation_dao_ = ReservationDao()
    _payment_dao_ = PaymentDao()
    _thrower_exceptions = ThrowerExceptions()
    _use_dao = UserDao()
    _MIN_AMOUNT = 10000
    _MAX_RESERVATION = 4
    _TYNE_COMMISSION = 0.15
    _WEEK_AS_DAYS = 7
    _DAY_ADJUSTMENT = 1
    _HOUR_AS_SECONDS = 3600
    _TYNE_LIMIT_HOUR = 2
    _email_service = EmailService()
    _branch_dao = BranchDao()
    _scheduler: BackgroundScheduler = scheduler

    def create_reservation_event(self, **kwargs):

        logger.info("Se inicia el evento de la reserva. Se envia email hacia sucursal para confirmar/cancelar")
        print(kwargs) # TODO: Eliminar

        # TODO: Enviar mensaje de reserva pendiente a confirmar/cancelar a sucursal, falta un endpoint con reserva id como dato
        # self._email_service.send_email(user=Constants.BRANCH, subject=EmailSubject) # TODO: Mensaje para cliente. Falta template

        self._scheduler.add_job(func=self.cancel_reservation, kwargs=kwargs,
                                id=kwargs.get('job_id'), misfire_grace_time=5, coalesce=True,
                                replace_existing=True, trigger='interval', seconds=15)  # TODO: Este job dura 15 minutos. 900 segundos

        logger.info("Evento reserva se actualiza a 15 minutos para anular reserva")

    def cancel_reservation(self, **kwargs):
        logger.info("Se inicia el evento de anulación de reserva")
        print(kwargs) # TODO: Eliminar
        self._scheduler.pause_job(kwargs.get('job_id'))
        print("SE ha pausado job " + kwargs.get('job_id'))
        self._scheduler.remove_job(kwargs.get('job_id'))
        print("SE ha eliminado job de cancelar reserva" + kwargs.get('job_id'))
        # TODO: Se podría dejar esta lógica en otro servicio ej ReservationEventService
        # TODO: Ver https://apscheduler.readthedocs.io/en/master/modules/triggers/interval.html#module-apscheduler.triggers.interval

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.LOCAL_NO_CONFIRMATION_TO_CLIENT,
                                       receiver_email=kwargs.get('client_email'))
        self._email_service.send_email(user=Constants.BRANCH, subject=EmailSubject.LOCAL_NO_CONFIRMATION_TO_LOCAL,
                                       receiver_email=kwargs.get('branch_email'))

        # TODO: Actualizar anulación de reserva en base de datos.

    # TODO: Función de prueba para verificar reservation evento
    def test_reservation_event(self, id: str):
        print("Entra a test reservation")
        kwargs: dict = {
            'job_id': id,
            'branch_email': 'tonyn.rome@gmail.com',
            'client_email': 'tonyn.rome@gmail.com',
            'reservation_id': 1
        }
        date: str = '2022-02-21'
        hour: str = '20:15'  # TODO: Cambiar para pruebas
        datetime_reservation = datetime.strptime(date + ' ' + hour, '%Y-%m-%d %H:%M').astimezone()
        current_datetime: datetime = datetime.now().astimezone()
        if datetime_reservation < current_datetime:
            raise CustomError(name=Constants.RESERVATION_DATETIME_ERROR,
                              detail=Constants.RESERVATION_DATETIME_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Fecha y/o hora de reserva no válida")

        difference_as_seconds: int = round((datetime_reservation - current_datetime).total_seconds())
        print("datetime de reserva: " + str(datetime_reservation) + " datetime actual: " + str(current_datetime))
        print("diferencia en fecha: " + str((datetime_reservation - current_datetime)))
        print("diferencia en segundos: " + str(difference_as_seconds))
        self._scheduler.add_job(func=self.create_reservation_event, kwargs=kwargs,
                                id=kwargs.get('job_id'), misfire_grace_time=5, coalesce=True,
                                replace_existing=True, trigger='interval', seconds=difference_as_seconds)

        print("Se inicia el job: " + id)

    async def create_reservation(self, client_id: int, new_reservation: NewReservationRequest, db: Session):
        logger.info("new_reservation: {}", dict(new_reservation))

        # TODO: Ver los links para template email con variables
        #  -  https://sabuhish.github.io/fastapi-mail/
        #  -  https://jinja2docs.readthedocs.io/en/stable/
        #  ¿Qué pasa si en el intervalo de tiempo de confirmación reserva el local cierra la sucursal o el día de la reserva?

        client: ClientEntity = self._client_dao_.get_client_by_id(client_id=client_id, db=db)

        reservation_count: int = self._reservation_dao_.\
            get_reservation_count_by_date(branch_id=new_reservation.branch_id,
                                          date_reservation=new_reservation.date, db=db)
        logger.info("reservation_count: {}", reservation_count)

        if reservation_count >= self._MAX_RESERVATION:
            raise CustomError(name=Constants.BRANCH_MAX_RESERVATION,
                              detail=Constants.CLIENT_UNAUTHORIZED,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause=f"Sucursal ya cuenta con el máximo de reservas para el día")

        request_reservation_date: datetime = datetime.now().astimezone()
        reservation_day: int = new_reservation.date.isoweekday() - self._DAY_ADJUSTMENT
        logger.info("reservation_day: {}", reservation_day)

        branch_schedule_entity = self._branch_dao.get_day_schedule(branch_id=new_reservation.branch_id,
                                                                   day=reservation_day, db=db)
        logger.info("Obtiene horario de sucursal: {}", branch_schedule_entity)

        if not branch_schedule_entity:
            raise CustomError(name=Constants.BRANCH_DAY_UNABLE,
                              detail=Constants.BRANCH_DAY_UNABLE_DETAIL,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Sucursal no disponible para el día requerido")

        is_valid_time = self._is_valid_hour(opening_hour=branch_schedule_entity.opening_hour,
                                            closing_hour=branch_schedule_entity.closing_hour,
                                            request_hour=new_reservation.hour)

        logger.info("is_valid_time: {}", is_valid_time)
        # TODO: Validar con front que devuelva la fecha solamente en campo date
        datetime_reservation: datetime = datetime.strptime(str(new_reservation.date.date()) + ' ' + new_reservation.hour,
                                                           '%Y-%m-%d %H:%M').astimezone()
        current_datetime: datetime = datetime.now().astimezone()

        if not is_valid_time or \
                (new_reservation.date - request_reservation_date).days > self._WEEK_AS_DAYS or \
                datetime_reservation < current_datetime:
            raise CustomError(name=Constants.RESERVATION_DATETIME_ERROR,
                              detail=Constants.RESERVATION_DATETIME_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Fecha y/o hora de reserva no válida")

        difference_as_seconds: int = round((datetime_reservation - current_datetime).total_seconds())
        logger.info("Diferencia en segundos: {}", difference_as_seconds)

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

        if amount < self._MIN_AMOUNT:
            raise CustomError(name=Constants.BUY_INVALID_ERROR,
                              detail=Constants.BUY_INVALID_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause=f"La compra debe ser mayor a {self._MIN_AMOUNT}")

        fifteen_percent: int = round(amount * self._TYNE_COMMISSION)
        logger.info("15% amount: {}", fifteen_percent)

        total_amount: int = amount + fifteen_percent
        logger.info("Tota amount: {}", total_amount)

        reservation_entity: ReservationEntity = self._create_reservation_entity(new_reservation=new_reservation,
                                                                                client_id=client_id, amount=amount,
                                                                                fifteen_percent=fifteen_percent)

        reservation_status = ReservationChangeStatusEntity()
        reservation_status.status_id = ReservationStatus.STARTED
        reservation_status.datetime = datetime.now().astimezone()

        reservation_id = self._reservation_dao_.create_reservation(reservation=reservation_status,
                                                                   reservation_status=reservation_status,
                                                                   products=reservation_products,
                                                                   db=db)

        response_khipu = self._khipu_service.create_link(amount=total_amount, payer_email=client.user.email,
                                                         transaction_id=reservation_entity.transaction_id)

        if response_khipu.status != status.HTTP_201_CREATED:
            # TODO: Persistir con change status = 3 la entidad
            await self._thrower_exceptions.throw_custom_exception(name=Constants.KHIPU_GET_ERROR,
                                                                  detail=Constants.KHIPU_GET_ERROR,
                                                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                  cause="Error obtener datos khipu")

        self._reservation_dao_.update_payment_id_reservation(reservation_id=reservation_id,
                                                             payment_id=response_khipu.payment_id,
                                                             db=db)
        logger.info("Se actualiza id de pago")

        reservation_status.status_id = ReservationStatus.IN_PROCESS
        reservation_status.datetime = datetime.now().astimezone()
        reservation_status.reservation_id = reservation_id
        self._reservation_dao_.update_reservation_status(reservation_status=reservation_status, db=db)

        response = ReservationResponse()
        response.url_payment = response_khipu.url
        response.reservation_id = reservation_id
        response.payment_id = response_khipu.payment_id

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.SUCCESSFUL_PAYMENT,
                                       receiver_email=client.user.email) # TODO: Agregar template. Actualizar archivo html
        logger.info("Se envia correo a cliente")

        branch_email: str = self._use_dao.get_email_by_branch(branch_id=new_reservation.branch_id, db=db)

        job_id: str = str(reservation_id)
        kwargs: dict = {
            'job_id': job_id,
            'branch_email': branch_email,
            'client_email': client.user.email,
            'reservation_change_status_id': reservation_status.id
        }

        self._scheduler.add_job(func=self.create_reservation_event, id=job_id, misfire_grace_time=5, coalesce=True,
                                replace_existing=True, trigger='interval', seconds=difference_as_seconds, kwargs=kwargs)

        logger.info("Se crea job evento reserva")

        # TODO: Agregar lógica para saber cuando da error, cambiar estado reserva a "con problemas" antes habia un try catch pero no aseguraba el reservation id
        reservation_status.status_id = ReservationStatus.NO_CONFIRMED
        reservation_status.datetime = datetime.now().astimezone()
        self._reservation_dao_.update_reservation_status(reservation_status=reservation_status, db=db)
        logger.info("Se actualiza estado de reserva a no confirmado")

        return response
    # TODO: Creo que se debe cambiar el nombre de esta función
    def _is_valid_hour(self, opening_hour: str, closing_hour: str, request_hour: str) -> bool:
        opening_hour_datetime = datetime.strptime(opening_hour, "%H:%M")
        closing_hour_datetime = datetime.strptime(closing_hour, "%H:%M")
        # TODO: Ver este link y guiarse tambien por la función de reserva evento
        #   https: // stackoverflow.com / questions / 34849188 / calculate - difference - between - two - time - in -hour
        if request_hour < opening_hour:
            difference_opening_seconds = opening_hour_datetime - datetime.strptime(request_hour, "%H:%M")
        else:
            difference_opening_seconds = datetime.strptime(request_hour, "%H:%M") - opening_hour_datetime

        difference_opening_hour = difference_opening_seconds.total_seconds() / self._HOUR_AS_SECONDS
        logger.info("difference_opening_hour: {}", difference_opening_hour)

        if request_hour < closing_hour:
            difference_closing_seconds = closing_hour_datetime - datetime.strptime(request_hour, "%H:%M")
        else:
            difference_closing_seconds = datetime.strptime(request_hour, "%H:%M") - closing_hour_datetime

        difference_closing_hour = difference_closing_seconds.total_seconds() / self._HOUR_AS_SECONDS
        logger.info("difference_closing_hour: {}", difference_closing_hour)

        # TODO: Menor 2 hrs de cierre O Mayor 2 horas de apertura
        return difference_opening_hour >= self._TYNE_LIMIT_HOUR and difference_closing_hour >= self._TYNE_LIMIT_HOUR

    def _create_reservation_product(self, product: ProductEntity, quantity: int) -> ReservationProductEntity:  #TODO: Se podría moder metodo a otro lado
        reservation_product = ReservationProductEntity()
        reservation_product.name_product = product.name
        reservation_product.category_product = product.category.name
        reservation_product.amount = product.amount
        reservation_product.quantity = quantity
        reservation_product.description = product.description
        return reservation_product

    def _create_reservation_entity(self, new_reservation: NewReservationRequest,
                                  client_id: int, amount: int, fifteen_percent: int) -> ReservationEntity: #TODO: Se podría moder metodo a otro lado
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

    async def get_reservations(self, client_id: int, db: Session) -> list:
        reservations = self._reservation_dao_.get_reservations(client_id, db)
        return reservations

    async def update_reservation(self, reservation_updated: UpdateReservationRequest,
                                 db: Session):

        # validate request
        reservation_updated.validate_fields()

        # get the reservation
        reservation = self._reservation_dao_.get_reservation(reservation_id=reservation_updated.reservation_id,
                                                             payment_id=reservation_updated.payment_id, db=db)

        if not reservation:
            raise CustomError(name="Reserva no existe",
                              detail="Error",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Reserva no existe")

        # verify if exists a payment with the same reservation id
        payment = self._payment_dao_.get_payment(reservation_id=reservation_updated.reservation_id, db=db)

        if payment:
            raise CustomError(name="Ya existe un pago asociado",
                              detail="Error",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Ya existe un pago asociado")

        # save the status pago cancelado or pago rechazado
        if reservation_updated.status.value == ReservationStatus.CANCELED_PAYMENT or \
                reservation_updated.status.value == ReservationStatus.REJECTED_PAYMENT or \
                reservation_updated.status.value == ReservationStatus.REJECTED_BY_LOCAL or \
                reservation_updated.status.value == ReservationStatus.CONFIRMED or \
                reservation_updated.status.value == ReservationStatus.SERVICED:
            reservation_status = ReservationChangeStatusEntity()
            reservation_status.status_id = reservation_updated.status.value
            reservation_status.datetime = datetime.now().astimezone()
            reservation_status.reservation_id = reservation_updated.reservation_id
            self._reservation_dao_.add_reservation_status(reservation_status=reservation_status, db=db)
            return SimpleResponse("Reserva actualizada correctamente")

        # get and verify the payment in khipu
        payment_khipu = self._khipu_service.verify_payment(reservation_updated.payment_id)

        # set data to create the payment and update the reservation status
        payment = PaymentEntity()
        payment.date = datetime.now().astimezone()
        payment.method = "Khipu"
        payment.amount = payment_khipu.amount
        payment.type_coin_id = 1
        payment.receipt_url = payment_khipu.receipt_url
        payment.reservation_id = reservation_updated.reservation_id

        reservation_status = ReservationChangeStatusEntity()
        reservation_status.status_id = ReservationStatus.SUCCESSFUL_PAYMENT
        reservation_status.datetime = datetime.now().astimezone()
        reservation_status.reservation_id = reservation_updated.reservation_id

        payment_response = self._payment_dao_.create_payment(payment=payment, reservation_status=reservation_status,
                                                             db=db)
        response = UpdateReservationResponse()
        response.payment_id = payment_response.id
        response.amount = payment_response.amount
        response.reservation_id = payment_response.reservation_id
        response.receipt_url = payment_response.receipt_url
        # TODO: ReservationEvent checkear si existe el evento de reserva con el id de reserva
        return response
