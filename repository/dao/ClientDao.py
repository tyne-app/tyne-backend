from configuration.database.database import SessionLocal
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity


class ClientDao:

    def find_client_by_email_user(self, email: str, db: SessionLocal):
        try:
            client = db.query(ClientEntity). \
                select_from(ClientEntity). \
                join(UserEntity, ClientEntity.id_user == UserEntity.id). \
                filter(UserEntity.email == email).first()
            return client
        except Exception as error:
            raise error
