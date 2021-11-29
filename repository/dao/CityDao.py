from sqlalchemy.orm import Session
from repository.entity.CityEntity import CityEntity


def get_cities(id_country: int, db: Session):
    return db \
        .query(CityEntity) \
        .filter(CityEntity.country_id == id_country) \
        .all()


def get_city_by_id(id_city: int, db: Session):
    return db \
        .query(CityEntity) \
        .filter(CityEntity.id == id_city) \
        .first()
