from sqlalchemy.orm import Session
from repository.entity.UserEntity import UserEntity


def login(email: str, password: str, db: Session):
    try:
        user = db.query(UserEntity)\
            .filter(UserEntity.email == email)\
            .filter(UserEntity.password == password)\
            .first()
        return user
    except Exception as error:
        raise error
    finally:
        db.close()

