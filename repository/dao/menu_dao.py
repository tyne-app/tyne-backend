from fastapi import status
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from exception.exceptions import CustomError
from repository.model import models
from repository.model.models import Category


def get_products_by_branch(db: Session, branch_id: int):
    try:
        return db.query(models.Product).filter(models.Product.branch_id == branch_id).all()
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


def save(db: Session, categories: list[Category]):
    try:
        db.add_all(categories)
        db.commit()
        return True

    except SQLAlchemyError as error:
        logger.error(error)
        raise CustomError(name="Error menu",
                          detail="BD error",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          cause=error.__cause__)
    except Exception as error:
        logger.error(error)
        raise CustomError(name="Error menu",
                          detail="BD error",
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          cause=error.__cause__)
