from sqlalchemy.orm import Session, joinedload
from repository.entity.ProductEntity import ProductEntity


class ProductDao:

    def get_products_by_ids(self, products_id: list[int], branch_id: int, db: Session) -> list[ProductEntity]:
        return db.query(ProductEntity) \
            .filter(ProductEntity.branch_id == branch_id) \
            .filter(ProductEntity.id.in_(products_id)) \
            .all()

    def save_all_products(self, db: Session, products):
        db.bulk_save_objects(products)
        db.commit()
        return True

    def save_all_products_menu(self, db: Session, seccions_list_entity, branch_id):
        db.query(ProductEntity).filter(ProductEntity.branch_id == branch_id).delete()

        for products in seccions_list_entity:
            db.bulk_save_objects(products)

        db.commit()
        return True

    def get_products_by_branch(self, db: Session, branch_id: int) -> ProductEntity:
        return db \
            .query(ProductEntity) \
            .options(joinedload(ProductEntity.category, innerjoin=True)) \
            .filter(ProductEntity.branch_id == branch_id) \
            .all()
