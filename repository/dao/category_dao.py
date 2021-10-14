from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from repository.entity.CategoryEntity import CategoryEntity


def get_by_id(db: Session, id_cat):
    return db.query(CategoryEntity).filter(CategoryEntity.id == id_cat).first()
