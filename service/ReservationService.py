from datetime import timezone, datetime

from sqlalchemy.orm import Session
from starlette import status

from dto.request.NewReservationRequest import NewReservationRequest
from enums.ReservationStatusEnum import ReservationStatusEnum
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.dao.Product2Dao import ProductDao
from repository.dao.ReservationDao import ReservationDao
from repository.entity.ClientEntity import ClientEntity
from repository.entity.ProductEntity import ProductEntity
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from repository.entity.ReservationEntity import ReservationEntity
from service.KhipuService import KhipuService


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

            for product in products:
                for x in reservation.products:
                    if product.id == x.id:
                        amount += x.quantity * (product.amount + product.commission_tyne)

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

            reservation_status = ReservationChangeStatusEntity()
            reservation_status.status_id = ReservationStatusEnum.reserva_iniciada.value
            reservation_status.datetime = datetime.now(tz=timezone.utc)
            reservation_status.reservation_id = entity.id

            # save reservation
            reservation_response = self._reservation_dao.create_reservation(reservation=entity,
                                                                            reservation_status=reservation_status,
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

        except Exception as error:

            if reservation_id > 0:
                change_status = ReservationChangeStatusEntity()
                change_status.status_id = ReservationStatusEnum.reserva_con_problemas.value
                change_status.datetime = datetime.now(tz=timezone.utc)
                change_status.reservation_id = reservation_id
                self._reservation_dao.add_reservation_status(reservation_status=change_status, db=db)

            raise error
