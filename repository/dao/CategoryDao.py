from sqlalchemy.orm import Session
from repository.entity.CategoryEntity import CategoryEntity


class CategoryDao:

    def get_categories(self, db: Session) -> list[CategoryEntity]:
        return db \
            .query(CategoryEntity) \
            .filter(CategoryEntity.is_active) \
            .order_by(CategoryEntity.order.asc()) \
            .all()
