from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from configuration.database import database
from repository.dao.CityDao import CityDao
from repository.dao.CountryDao import CountryDao
from repository.dao.StateDao import StateDao
from util.ThrowerExceptions import ThrowerExceptions

territory_controller = APIRouter(
    prefix="/v1/territories",
    tags=["Territories"]
)

_throwerExceptions = ThrowerExceptions()
_city_dao_ = CityDao()
_state_dao_ = StateDao()
_country_dao_ = CountryDao()


@territory_controller.get(
    '/countries',
    status_code=status.HTTP_200_OK
)
async def get_countries(response: Response, db: Session = Depends(database.get_data_base)):
    countries = _country_dao_.get_all_countries(db)

    if len(countries) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return countries


@territory_controller.get(
    '/countries/{id_country}',
    status_code=status.HTTP_200_OK
)
async def get_country(response: Response, id_country: int, db: Session = Depends(database.get_data_base)):
    country = _country_dao_.get_country_by_id(id_country, db)

    if country is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return country


@territory_controller.get(
    '/countries/{id_country}/cities',
    status_code=status.HTTP_200_OK
)
async def get_cities_by_country(response: Response, id_country: int, db: Session = Depends(database.get_data_base)):
    cities = _city_dao_.get_cities(id_country, db)

    if len(cities) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return cities


@territory_controller.get(
    '/cities/{id_city}',
    status_code=status.HTTP_200_OK
)
async def get_city(response: Response, id_city: int, db: Session = Depends(database.get_data_base)):
    city = _city_dao_.get_city_by_id(id_city, db)

    if city is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return city


@territory_controller.get(
    '/cities/{id_city}/states',
    status_code=status.HTTP_200_OK
)
async def get_states_by_city(response: Response, id_city: int, db: Session = Depends(database.get_data_base)):
    states = _state_dao_.get_states(id_city, db)

    if len(states) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return states


@territory_controller.get(
    '/state/{id_state}',
    status_code=status.HTTP_200_OK
)
async def get_state(response: Response, id_state: int, db: Session = Depends(database.get_data_base)):
    state = _state_dao_.get_state_by_id(id_state, db)

    if state is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return state
