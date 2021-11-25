from sqlalchemy.orm import Session

from repository.entity.CategoryEntity import CategoryEntity


def get_by_id(db: Session, id_cat):
    return db \
        .query(CategoryEntity) \
        .filter(CategoryEntity.id == id_cat) \
        .first()


def get_all(db: Session):
    return db \
        .query(CategoryEntity) \
        .filter(CategoryEntity.is_active == 'true') \
        .order_by(CategoryEntity.order.asc()) \
        .all()
