from sqlalchemy.orm import Session
from repository.entity.CountryEntity import CountryEntity


class CountryDao:

    def get_all_countries(self, db: Session) -> list[CountryEntity]:
        return db \
            .query(CountryEntity) \
            .all()

    def get_country_by_id(self, id_country: int, db: Session) -> CountryEntity:
        return db \
            .query(CountryEntity) \
            .filter(CountryEntity.id == id_country) \
            .first()
