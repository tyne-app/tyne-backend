from sqlalchemy.orm import Session
from repository.entity.CityEntity import CityEntity


def get_cities(id_country: int, db: Session):
    try:
        cities = db.query(CityEntity).filter(CityEntity.country_id == id_country).all()
        return cities
    except Exception as error:
        return error.args[0]
    finally:
        db.close()


def get_city_by_id(id_city: int, db: Session):
    try:
        city = db.query(CityEntity).filter(CityEntity.id == id_city).first()
        return city
    except Exception as error:
        return error.args[0]
    finally:
        db.close()
