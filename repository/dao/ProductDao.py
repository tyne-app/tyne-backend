from sqlalchemy.orm import Session, joinedload

from repository.entity.ProductEntity import ProductEntity


def save_all_products(db: Session, products):
    db.bulk_save_objects(products)
    db.commit()
    return True


def save_all_products_menu(db: Session, seccions_list_entity, branch_id):
    db.query(ProductEntity).filter(ProductEntity.branch_id == branch_id).delete()

    for products in seccions_list_entity:
        db.bulk_save_objects(products)

    db.commit()
    return True


def get_products_by_branch(db: Session, branch_id: int):
    return db \
        .query(ProductEntity) \
        .options(joinedload(ProductEntity.category, innerjoin=True)) \
        .filter(ProductEntity.branch_id == branch_id) \
        .all()
