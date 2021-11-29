from sqlalchemy.orm import Session

from repository.entity.StateEntity import StateEntity


def get_states(id_city: int, db: Session):
    return db \
        .query(StateEntity) \
        .filter(StateEntity.city_id == id_city) \
        .all()


def get_state_by_id(id_state: int, db: Session):
    return db \
        .query(StateEntity) \
        .filter(StateEntity.id == id_state) \
        .first()
