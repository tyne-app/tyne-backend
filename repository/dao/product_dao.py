from fastapi import status
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from exception.exceptions import CustomError

from repository.entity.BranchEntity import BranchEntity  # TODO: NO eliminar
from repository.entity.ProductEntity import ProductEntity


def save_all_products(db: Session, products):
    try:
        db.bulk_save_objects(products)
        db.commit()
        return True

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


def save_all_products_menu(db: Session, seccions_list_entity, branch_id):
    try:

        db.query(ProductEntity).filter(ProductEntity.branch_id == branch_id).delete()

        for products in seccions_list_entity:
            db.bulk_save_objects(products)

        db.commit()
        return True

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

def get_products_by_branch(db: Session, branch_id: int):
    try:
        return db \
            .query(ProductEntity) \
            .options(joinedload(ProductEntity.category, innerjoin=True)) \
            .filter(ProductEntity.branch_id == branch_id) \
            .all()

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
