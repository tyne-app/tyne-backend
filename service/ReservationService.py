from sqlalchemy.orm import Session
from starlette import status

from dto.request.NewReservationRequest import NewReservationRequest
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.dao.Product2Dao import ProductDao
from repository.entity.ClientEntity import ClientEntity
from repository.entity.ProductEntity import ProductEntity
from service.KhipuService import KhipuService


class ReservationService:
    _client_dao_ = ClientDao()
    _khipu_service = KhipuService()
    _product_dao_ = ProductDao()

    def create_reservation(self, client_id: int, reservation: NewReservationRequest, db: Session):

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

        response_khipu = self._khipu_service.create_link(amount=amount, payer_email=client.user.email,
                                                         transaction_id="DDAAD2343")

