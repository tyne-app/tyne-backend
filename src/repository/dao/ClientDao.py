from sqlalchemy.orm import Session

from src.dto.request.ClientRequest import ClientRequest
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.UserEntity import UserEntity


class ClientDao:

    def find_client_by_email_user(self, email: str, db: Session) -> ClientEntity:
        return db \
            .query(ClientEntity) \
            .select_from(ClientEntity) \
            .join(UserEntity, ClientEntity.id_user == UserEntity.id) \
            .filter(UserEntity.email == email) \
            .first()

    def get_client_by_id(self, client_id: int, db: Session) -> ClientEntity:
        return db \
            .query(ClientEntity) \
            .filter(ClientEntity.id == client_id) \
            .first()

    def create_client(self, client_req: ClientRequest, id_login_created: int, db: Session):
        db.add(client_req.to_entity(id_login_created))
        db.commit()
        return True

    def create_client_v2(self, client: ClientEntity, db: Session):
        try:
            db.add(client.user)
            db.flush()

            client.id_user = client.user.id
            db.add(client)

            db.commit()
            return True
        except Exception as ex:
            db.rollback()
            raise ex
