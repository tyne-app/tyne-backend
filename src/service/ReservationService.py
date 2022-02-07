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
from src.enums.ReservationStatusEnum import ReservationStatusEnum
from src.exception.exceptions import CustomError
from src.repository.dao.ClientDao import ClientDao
from src.repository.dao.PaymentDao import PaymentDao
from src.repository.dao.ProductDao import ProductDao
from src.repository.dao.ReservationDao import ReservationDao
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.PaymentEntity import PaymentEntity
from src.repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from src.repository.entity.ReservationEntity import ReservationEntity
from src.repository.entity.ReservationProductEntity import ReservationProductEntity
from src.service.KhipuService import KhipuService
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions


class ReservationService:
    _client_dao_ = ClientDao()
    _khipu_service = KhipuService()
    _product_dao_ = ProductDao()
    _reservation_dao_ = ReservationDao()
    _payment_dao_ = PaymentDao()
    _thrower_exceptions = ThrowerExceptions()

    async def create_reservation(self, client_id: int, reservation: NewReservationRequest, db: Session):

        reservation_id = 0

        try:
            await reservation.validate_fields()

            products = self._product_dao_.get_products_by_ids(
                products_id=reservation.get_products_ids(),
                branch_id=reservation.branch_id, db=db)

            if not products:
                await self._thrower_exceptions.throw_custom_exception(name=Constants.PRODUCT_NOT_EXIST,
                                                                      detail=Constants.PRODUCT_NOT_EXIST,
                                                                      status_code=status.HTTP_400_BAD_REQUEST,
                                                                      cause=f"No existen productos con branch_id {reservation.branch_id} para la reserva")

            client: ClientEntity = self._client_dao_.get_client_by_id(client_id=client_id, db=db)

            if client is None:
                await self._thrower_exceptions.throw_custom_exception(name=Constants.CLIENT_NOT_EXIST,
                                                                      detail=Constants.CLIENT_NOT_EXIST,
                                                                      status_code=status.HTTP_400_BAD_REQUEST,
                                                                      cause=f"Cliente con el id {client_id} no existe para crear la reserva")

            if not client.user.is_active:
                await self._thrower_exceptions.throw_custom_exception(name=Constants.CLIENT_UNAUTHORIZED,
                                                                      detail=Constants.CLIENT_UNAUTHORIZED,
                                                                      status_code=status.HTTP_401_UNAUTHORIZED,
                                                                      cause=f"Cliente con el id {client_id} esta inactivo")

            amount = 0

            reservation_products: list[ReservationProductEntity] = []

            for product in products:
                for x in reservation.products:
                    if product.id == x.id:
                        amount += x.quantity * (product.amount + product.commission_tyne)
                        reservation_product = ReservationProductEntity()
                        reservation_product.name_product = product.name
                        reservation_product.category_product = product.category.name
                        reservation_product.amount = product.amount
                        reservation_product.commission_tyne = product.commission_tyne
                        reservation_product.quantity = x.quantity
                        reservation_product.description = product.description
                        reservation_products.append(reservation_product)

            amount = round(amount)
            MIN_BUY: int = 10000
            if amount < MIN_BUY:
                await self._thrower_exceptions.throw_custom_exception(name=Constants.BUY_INVALID_ERROR,
                                                                      detail=Constants.BUY_INVALID_ERROR,
                                                                      status_code=status.HTTP_400_BAD_REQUEST,
                                                                      cause=f"La compra debe ser mayor a {str(MIN_BUY)}")

            entity = ReservationEntity()
            entity.reservation_date = reservation.date
            entity.preference = reservation.preference
            entity.client_id = client_id
            entity.branch_id = reservation.branch_id
            entity.people = reservation.people
            entity.hour = reservation.hour
            entity.transaction_id = str(uuid.uuid4())

            reservation_status = ReservationChangeStatusEntity()
            reservation_status.status_id = ReservationStatusEnum.reserva_iniciada.value
            reservation_status.datetime = datetime.now(tz=timezone.utc)
            reservation_status.reservation_id = entity.id

            # save reservation
            reservation_response = self._reservation_dao_.create_reservation(reservation=entity,
                                                                             reservation_status=reservation_status,
                                                                             products=reservation_products,
                                                                             db=db)

            reservation_id = reservation_response.id

            # request payment link
            response_khipu = self._khipu_service.create_link(amount=amount, payer_email=client.user.email,
                                                             transaction_id=entity.transaction_id)

            if response_khipu.status != 201:
                await self._thrower_exceptions.throw_custom_exception(name=Constants.KHIPU_GET_ERROR,
                                                                      detail=Constants.KHIPU_GET_ERROR,
                                                                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                      cause="Error obtener datos khipu")

            # update reservation with payment_id from khipu
            self._reservation_dao_.update_payment_id_reservation(reservation_id=reservation_id,
                                                                 payment_id=response_khipu.payment_id,
                                                                 db=db)

            # add new reservation change status
            change_status = ReservationChangeStatusEntity()
            change_status.status_id = ReservationStatusEnum.reserva_en_proceso.value
            change_status.datetime = datetime.now(tz=timezone.utc)
            change_status.reservation_id = reservation_id
            self._reservation_dao_.add_reservation_status(reservation_status=change_status, db=db)

            response = ReservationResponse()
            response.url_payment = response_khipu.url
            response.reservation_id = reservation_id
            response.payment_id = response_khipu.payment_id
            return response

        except Exception as error:

            if reservation_id > 0:
                change_status = ReservationChangeStatusEntity()
                change_status.status_id = ReservationStatusEnum.reserva_con_problemas.value
                change_status.datetime = datetime.now(tz=timezone.utc)
                change_status.reservation_id = reservation_id
                self._reservation_dao_.add_reservation_status(reservation_status=change_status, db=db)

            raise error

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
        if reservation_updated.status.value == ReservationStatusEnum.pago_cancelado.value or \
                reservation_updated.status.value == ReservationStatusEnum.pago_rechazado.value or \
                reservation_updated.status.value == ReservationStatusEnum.cancelado_local.value or \
                reservation_updated.status.value == ReservationStatusEnum.reserva_confirmada.value or \
                reservation_updated.status.value == ReservationStatusEnum.reserva_atendida.value:
            reservation_status = ReservationChangeStatusEntity()
            reservation_status.status_id = reservation_updated.status.value
            reservation_status.datetime = datetime.now(tz=timezone.utc)
            reservation_status.reservation_id = reservation_updated.reservation_id
            self._reservation_dao_.add_reservation_status(reservation_status=reservation_status, db=db)
            return SimpleResponse("Reserva actualizada correctamente")

        # get and verify the payment in khipu
        payment_khipu = self._khipu_service.verify_payment(reservation_updated.payment_id)

        # set data to create the payment and update the reservation status
        payment = PaymentEntity()
        payment.date = datetime.now(tz=timezone.utc)
        payment.method = "Khipu"
        payment.amount = payment_khipu.amount
        payment.type_coin_id = 1
        payment.receipt_url = payment_khipu.receipt_url
        payment.reservation_id = reservation_updated.reservation_id

        reservation_status = ReservationChangeStatusEntity()
        reservation_status.status_id = ReservationStatusEnum.pago_exitoso.value
        reservation_status.datetime = datetime.now(tz=timezone.utc)
        reservation_status.reservation_id = reservation_updated.reservation_id

        payment_response = self._payment_dao_.create_payment(payment=payment, reservation_status=reservation_status,
                                                             db=db)
        response = UpdateReservationResponse()
        response.payment_id = payment_response.id
        response.amount = payment_response.amount
        response.reservation_id = payment_response.reservation_id
        response.receipt_url = payment_response.receipt_url

        return response
