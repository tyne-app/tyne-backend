from configuration.database.database import SessionLocal
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity


class ClientDao:

    @classmethod
    def find_client_by_email_user(cls, email: str, db: SessionLocal):
        try:
            client = db.query(ClientEntity). \
                select_from(ClientEntity). \
                join(UserEntity, ClientEntity.id_user == UserEntity.id). \
                filter(UserEntity.email == email).first()
            return client
        except Exception as error:
            raise error

    @classmethod
    def get_client(cls, client_id: int, db: SessionLocal):
        try:
            client = db.query(ClientEntity). \
                filter(ClientEntity.id == client_id).first()
            return client
        except Exception as error:
            raise error
