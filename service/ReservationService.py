from sqlalchemy.orm import Session
from starlette import status

from dto.request.NewReservationRequest import NewReservationRequest
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.entity.ClientEntity import ClientEntity


class ReservationService:
    _client_dao_ = ClientDao()

    def create_reservation(self, client_id: int, reservation: NewReservationRequest, db: Session):
        # validar que se pueda reservar en el local
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
                              cause="Cliente no existe")


    pass
