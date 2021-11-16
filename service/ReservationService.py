from datetime import timezone, datetime

from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from dto.request.NewReservationRequest import NewReservationRequest
from dto.request.LocalReservationsRequest import LocalReservationRequest
from dto.response.ReservationResponse import ReservationResponse
from dto.response.LocalReservationsResponse import LocalReservationsResponse
from dto.response.ReservationDetailResponse import ReservationDetailResponse
from enums.ReservationStatusEnum import ReservationStatusEnum
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.dao.Product2Dao import ProductDao
from repository.dao.ReservationDao import ReservationDao
from repository.entity.ClientEntity import ClientEntity
from repository.entity.ProductEntity import ProductEntity
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from repository.entity.ReservationEntity import ReservationEntity
from repository.entity.ReservationProductEntity import ReservationProductEntity
from service.KhipuService import KhipuService

from dto.dto import GenericDTO as responseDTO


class ReservationService:
    _client_dao_ = ClientDao()
    _khipu_service = KhipuService()
    _product_dao_ = ProductDao()
    _reservation_dao = ReservationDao()

    def create_reservation(self, client_id: int, reservation: NewReservationRequest, db: Session):

        reservation_id = 0

        try:
            reservation.validate_fields()

            products: list[ProductEntity] = self._product_dao_.get_products_by_ids(
                products_id=reservation.get_products_ids(),
                branch_id=reservation.branch_id, db=db)

            if not products:
                raise CustomError(name="No existen productos",
                                  detail="Validación",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause="No existen productos")

            client: ClientEntity = self._client_dao_.get_client(client_id=client_id, db=db)

            if client is None:
                raise CustomError(name="Cliente no existe",
                                  detail="Validación",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause="Cliente no existe")

            if not client.user.is_active:
                raise CustomError(name="Cliente no autorizado",
                                  detail="Validación",
                                  status_code=status.HTTP_401_UNAUTHORIZED,
                                  cause="Cliente no autorizado")

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
            min_buy: int = 10000
            if amount < min_buy:
                raise CustomError(name="Compra no válida",
                                  detail="Validación",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause="La compra debe ser mayor a " + str(min_buy))

            entity = ReservationEntity()
            entity.reservation_date = reservation.date
            entity.preference = reservation.preference
            entity.client_id = client_id
            entity.branch_id = reservation.branch_id
            entity.people = reservation.people
            entity.hour = reservation.hour

            reservation_status = ReservationChangeStatusEntity()
            reservation_status.status_id = ReservationStatusEnum.reserva_iniciada.value
            reservation_status.datetime = datetime.now(tz=timezone.utc)
            reservation_status.reservation_id = entity.id

            # save reservation
            reservation_response = self._reservation_dao.create_reservation(reservation=entity,
                                                                            reservation_status=reservation_status,
                                                                            products=reservation_products,
                                                                            db=db)

            reservation_id = reservation_response.id

            # request payment link
            response_khipu = self._khipu_service.create_link(amount=amount, payer_email=client.user.email,
                                                             transaction_id="UID-122233")

            if response_khipu.status != 201:
                raise CustomError(name="Error obtener datos khipu",
                                  detail="Khipu error",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause="Error obtener datos khipu")

            # update reservation with payment_id from khipu
            self._reservation_dao.update_payment_id_reservation(reservation_id=reservation_id,
                                                                payment_id=response_khipu.payment_id, db=db)

            # add new reservation change status
            change_status = ReservationChangeStatusEntity()
            change_status.status_id = ReservationStatusEnum.reserva_en_proceso.value
            change_status.datetime = datetime.now(tz=timezone.utc)
            change_status.reservation_id = reservation_id
            self._reservation_dao.add_reservation_status(reservation_status=change_status, db=db)

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
                self._reservation_dao.add_reservation_status(reservation_status=change_status, db=db)

            raise error

    @classmethod
    def local_reservations(cls, branch_id: int,
                           reservation_date: datetime,
                           result_for_page: int,
                           page_number: int,
                           status_reservation: int, db):

        local_reservation_request = LocalReservationRequest()
        local_reservation_request.reservation_date = reservation_date
        local_reservation_request.result_for_page = result_for_page
        local_reservation_request.page_number = page_number
        local_reservation_request.status_reservation = status_reservation

        local_reservation_request.validate_fields(local_reservation_request)

        reservations = ReservationDao.local_reservations(db
                                                         , branch_id
                                                         , reservation_date
                                                         , status_reservation)

        reservations_date = ReservationDao.local_reservations_date(db
                                                                   , branch_id
                                                                   , status_reservation
                                                                   , reservation_date
                                                                   , result_for_page
                                                                   , page_number)

        local_reservations_response = LocalReservationsResponse()
        response = local_reservations_response.local_reservations(reservations,
                                                                  reservations_date,
                                                                  result_for_page,
                                                                  page_number)
        return response

    @classmethod
    def reservation_detail(cls, reservation_id: int, db):

        if reservation_id == 0:
            raise CustomError(name="Validación",
                              detail="No se han encontrado datos de la reserva",
                              status_code=status.HTTP_204_NO_CONTENT,
                              cause="No se han encontrado datos de la reserva")

        reservations = ReservationDao.reservation_detail(db, reservation_id)

        reservation_detail = ReservationDetailResponse()
        response = reservation_detail.reservation_detail(reservations)
        return response

    def get_reservations(self, client_id: int, db: Session):
        try:
            reservations = self._reservation_dao.get_reservations(client_id, db)

            if not reservations:
                raise CustomError(name="Error get_reservation",
                                  detail="reservations not found",
                                  status_code=status.HTTP_204_NO_CONTENT)

            response = responseDTO()
            response.data = reservations
            return response.__dict__

        except CustomError as error:
            logger.error(error.detail)
            raise CustomError(name=error.name,
                              detail=error.detail,
                              status_code=error.status_code)

        except Exception as e:
            logger.error(e)
            raise CustomError(name="Error al obtener reservas",
                              detail="service Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="Error al obtener reservas")
