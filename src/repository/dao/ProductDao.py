from sqlalchemy.orm import Session, joinedload
from src.repository.entity.ProductEntity import ProductEntity


class ProductDao:

    def get_products_by_ids(self, products_id: list[int], branch_id: int, db: Session) -> list[ProductEntity]:
        return db.query(ProductEntity) \
            .filter(ProductEntity.branch_id == branch_id) \
            .filter(ProductEntity.id.in_(products_id)) \
            .all()

    def save_all_products(self, db: Session, products):  # TODO Parece que esto no se ocupa, eliminarlo.
        db.bulk_save_objects(products)
        db.commit()
        return True

    def save_all_products_menu(self, branch_id: int, sections_list_entity: list, db: Session) -> None:

        products: list
        product: ProductEntity

        for products_list in sections_list_entity:

            products_to_insert: list = []

            for product in products_list:
                product_exists = db.query(ProductEntity.id)\
                    .filter(ProductEntity.name == product.name)\
                    .filter(ProductEntity.category_id == product.category_id)\
                    .filter(ProductEntity.branch_id == branch_id)\
                    .first()

                if not product_exists:
                    products_to_insert.append(product)

            if products_to_insert:
                db.bulk_save_objects(products_list)

        db.commit()

    def get_products_by_branch(self, db: Session, branch_id: int) -> ProductEntity:
        return db \
            .query(ProductEntity) \
            .options(joinedload(ProductEntity.category, innerjoin=True)) \
            .filter(ProductEntity.branch_id == branch_id) \
            .all()
