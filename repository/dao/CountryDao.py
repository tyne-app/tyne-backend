from sqlalchemy.orm import Session
from repository.entity.CountryEntity import CountryEntity


def get_all_countries(db: Session):
    try:
        countries = db.query(CountryEntity).all()
        return countries
    except Exception as error:
        return error.args[0]
    finally:
        db.close()


def get_country_by_id(id_country: int, db: Session):
    try:
        country = db.query(CountryEntity).filter(CountryEntity.id == id_country).first()
        return country
    except Exception as error:
        return error.args[0]
    finally:
        db.close()
