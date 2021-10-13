from fastapi import status
from loguru import logger
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload


from exception.exceptions import CustomError
from repository.entity.ProductEntity import ProductEntity


def save_all_products(db: Session, products, branch_id):
    try:
        # for product in products:
        #     productDB = db.query(ProductEntity).filter(ProductEntity.id == product.id).first()
        #
        #     productDB.name = product.name
        #     productDB.description = product.description
        #     productDB.url_image = product.url_image
        #     productDB.amount = product.amount
        #     productDB.commission_tyne = product.commission_tyne
        #
        #     db.add(productDB)
        #     db.commit()
        #
        # return True

        # db.delete(ProductEntity).filter(ProductEntity.branch_id == 3)
        # db.commit()

        db.query(ProductEntity).filter(ProductEntity.branch_id == 3).delete()
        db.commit()

        # TODO: solucionar error al guardar
        db.bulk_save_objects(products)

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
        return db\
            .query(ProductEntity).options(joinedload(ProductEntity.category, innerjoin=True))\
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
