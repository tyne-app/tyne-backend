from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from configuration.database.database import SessionLocal
from exception.exceptions import CustomError
from repository.entity.OpinionEntity import OpinionEntity


class OpinionDao:

    @classmethod
    def find_by_branch_id(cls, db: SessionLocal, branch_id: int):
        try:
            options = db \
                .query(OpinionEntity) \
                .filter(OpinionEntity.branch_id == branch_id) \
                .all()

            return options

        except SQLAlchemyError as error:
            logger.error(error)
            raise CustomError(name="Error OpicionDao",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)

        except Exception as error:
            logger.error(error)
            raise CustomError(name="Error OpicionDao",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)
