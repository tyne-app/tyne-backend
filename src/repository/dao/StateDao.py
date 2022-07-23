from sqlalchemy.orm import Session
from src.repository.entity.StateEntity import StateEntity
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.BranchImageEntity import BranchImageEntity
from src.repository.entity.BranchScheduleEntity import BranchScheduleEntity
from src.repository.entity.ProductEntity import ProductEntity


class StateDao:

    def get_states(self, city_id: int, db: Session) -> list[StateEntity]:
        return db \
            .query(StateEntity) \
            .filter(StateEntity.city_id == city_id).all()

    def get_state_by_id(self, id_state: int, db: Session) -> StateEntity:
        return db \
            .query(StateEntity) \
            .filter(StateEntity.id == id_state) \
            .first()

    def get_available_states(self, city_id: int, db: Session) -> list[StateEntity]:
        return db.query(StateEntity) \
            .join(BranchEntity, BranchEntity.state_id == StateEntity.id) \
            .join(BranchImageEntity, BranchImageEntity.branch_id == BranchEntity.id) \
            .join(ProductEntity, ProductEntity.branch_id == BranchEntity.id) \
            .join(BranchScheduleEntity, BranchScheduleEntity.branch_id == BranchEntity.id) \
            .filter(StateEntity.city_id == city_id) \
            .filter(BranchScheduleEntity.active) \
            .order_by(StateEntity.name.asc()) \
            .all()
