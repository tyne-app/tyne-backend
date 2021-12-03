from sqlalchemy.orm import Session
from repository.entity.StateEntity import StateEntity


class StateDao:

    def get_states(self, id_city: int, db: Session) -> list[StateEntity]:
        return db \
            .query(StateEntity) \
            .filter(StateEntity.city_id == id_city) \
            .all()

    def get_state_by_id(self, id_state: int, db: Session) -> StateEntity:
        return db \
            .query(StateEntity) \
            .filter(StateEntity.id == id_state) \
            .first()
