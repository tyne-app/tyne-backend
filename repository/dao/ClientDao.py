from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from configuration.database.database import SessionLocal
from dto.request.ClientRequestDTO import ClientRequestDTO
from exception.exceptions import CustomError
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

    @classmethod
    def create_client(cls, client_req: ClientRequestDTO, id_login_created: int, db: SessionLocal):
        try:
            db.add(client_req.to_entity(id_login_created))
            db.commit()
            return True

        except SQLAlchemyError as error:
            logger.error(error)
            raise CustomError(name="Error create_client",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)

        except Exception as error:
            logger.error(error)
            raise CustomError(name="Error create_client",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)

    @classmethod
    def create_client_v2(cls, client: ClientEntity, db: Session):
        try:
            db.add(client.user)
            db.flush()

            client.id_user = client.user.id
            db.add(client)

            db.commit()
            return True

        except Exception as error:
            logger.error(error)
            db.rollback()
            raise CustomError(name="Error create_client",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)
