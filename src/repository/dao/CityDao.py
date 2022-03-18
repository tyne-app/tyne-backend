from sqlalchemy.orm import Session
from src.repository.entity.CityEntity import CityEntity


class CityDao:

    def get_cities(self, id_country: int, db: Session) -> list[CityEntity]:
        return db \
            .query(CityEntity) \
            .filter(CityEntity.country_id == id_country, CityEntity.id == 7) \
            .all()

    def get_city_by_id(self, id_city: int, db: Session) -> CityEntity:
        return db \
            .query(CityEntity) \
            .filter(CityEntity.id == id_city) \
            .first()
