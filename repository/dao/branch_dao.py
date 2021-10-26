from fastapi import status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from exception.exceptions import CustomError

from repository.entity.BranchEntity import BranchEntity  # TODO: NO eliminar


def get_branch_by_id(db: Session, branch_id):
    try:
        branch = db \
            .query(BranchEntity) \
            .filter(BranchEntity.id == branch_id).first()
            # .options(joinedload(BranchEntity.opinion_branch, innerjoin=True)) \

        return branch

    except SQLAlchemyError as error:
        logger.error(error)
        raise CustomError(name="Error products",
                          detail="BD error",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          cause=error.__cause__)
    except Exception as error:
        logger.error(error)
        raise CustomError(name="Error products",
                          detail="BD error",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          cause=error.__cause__)
    finally:
        db.close()
