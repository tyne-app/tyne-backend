from sqlalchemy.orm import Session

from configuration.database.database import SessionLocal
from dto.request.ClientRequestDTO import ClientRequestDTO
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity


class ClientDao:

    @classmethod
    def find_client_by_email_user(cls, email: str, db: SessionLocal):
        return db \
            .query(ClientEntity) \
            .select_from(ClientEntity) \
            .join(UserEntity, ClientEntity.id_user == UserEntity.id) \
            .filter(UserEntity.email == email) \
            .first()

    @classmethod
    def get_client_by_id(cls, client_id: int, db: SessionLocal):
        return db \
            .query(ClientEntity) \
            .filter(ClientEntity.id == client_id) \
            .first()

    @classmethod
    def create_client(cls, client_req: ClientRequestDTO, id_login_created: int, db: SessionLocal):
        db.add(client_req.to_entity(id_login_created))
        db.commit()
        return True

    @classmethod
    def create_client_v2(cls, client: ClientEntity, db: Session):
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
