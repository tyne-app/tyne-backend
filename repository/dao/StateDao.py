from sqlalchemy.orm import Session
from repository.entity.StateEntity import StateEntity


def get_states(id_city: int, db: Session):
    try:
        states = db.query(StateEntity).filter(StateEntity.city_id == id_city).all()
        return states
    except Exception as error:
        return error.args[0]
    finally:
        db.close()


def get_state_by_id(id_state: int, db: Session):
    try:
        city = db.query(StateEntity).filter(StateEntity.id == id_state).first()
        return city
    except Exception as error:
        return error.args[0]
    finally:
        db.close()