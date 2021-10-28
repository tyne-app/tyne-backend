from sqlalchemy.orm import Session

from repository.entity.ProductEntity import ProductEntity


class ProductDao:

    @classmethod
    def get_products_by_ids(cls, products_id: list[int], branch_id: int, db: Session):
        return db.query(ProductEntity)\
            .filter(ProductEntity.branch_id == branch_id)\
            .filter(ProductEntity.id.in_(products_id)).all()