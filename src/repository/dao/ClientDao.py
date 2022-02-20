from fastapi import status
from sqlalchemy.orm import Session
from loguru import logger
from src.dto.request.ClientRequest import ClientRequest
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.UserEntity import UserEntity
from src.exception.exceptions import CustomError
from sqlalchemy.exc import IntegrityError
from src.util.Constants import Constants


class ClientDao:

    def create_account(self, user_entity: UserEntity, client_entity: ClientEntity, db: Session):
        try:
            db.add(user_entity)
            db.flush()
            client_entity.id_user = user_entity.id
            db.add(client_entity)
            db.commit()
        except IntegrityError as err:
            print("Integration error")
            db.rollback()
            logger.info("Integrity error: {}", err)
            raise CustomError(name=Constants.EMAIL_INVALID_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              detail=Constants.USER_EMAIL_EXIST,
                              cause=Constants.USER_EMAIL_EXIST)
        except Exception as ex:
            print("Excepciones")
            db.rollback()
            raise ex

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
