from sqlalchemy.orm import Session
from repository.entity.CategoryEntity import CategoryEntity


class CategoryDao:

    def get_categories(self, db: Session):
        return db \
            .query(CategoryEntity) \
            .filter(CategoryEntity.is_active == 'true') \
            .order_by(CategoryEntity.order.asc()) \
            .all()