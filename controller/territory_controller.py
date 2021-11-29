from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session

from configuration.database import database
from repository.dao.CityDao import get_cities, get_city_by_id
from repository.dao.CountryDao import get_all_countries, get_country_by_id
from repository.dao.StateDao import get_states, get_state_by_id
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions

territory_controller = APIRouter(
    prefix="/v1/territories",
    tags=["Territories"]
)

_throwerExceptions = ThrowerExceptions()


@territory_controller.get(
    '/countries',
    status_code=status.HTTP_200_OK
)
async def get_countries(response: Response, db: Session = Depends(database.get_data_base)):
    countries = get_all_countries(db)

    if len(countries) == 0:
        await _throwerExceptions.throw_custom_exception(name=Constants.COUNTRY_NOT_FOUND_ERROR,
                                                        detail=Constants.COUNTRY_NOT_FOUND_ERROR,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return countries


@territory_controller.get(
    '/countries/{id_country}',
    status_code=status.HTTP_200_OK
)
async def get_country(response: Response, id_country: int, db: Session = Depends(database.get_data_base)):
    countries = get_country_by_id(id_country, db)

    if countries is None:
        await _throwerExceptions.throw_custom_exception(name=Constants.COUNTRY_NOT_FOUND_ERROR,
                                                        detail=Constants.COUNTRY_NOT_FOUND_ERROR,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return countries


@territory_controller.get(
    '/countries/{id_country}/cities',
    status_code=status.HTTP_200_OK
)
async def get_cities_by_country(response: Response, id_country: int, db: Session = Depends(database.get_data_base)):
    cities = get_cities(id_country, db)

    if len(cities) == 0:
        await _throwerExceptions.throw_custom_exception(name=Constants.CITIES_NOT_FOUND_ERROR,
                                                        detail=Constants.CITIES_NOT_FOUND_ERROR,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return cities


@territory_controller.get(
    '/cities/{id_city}',
    status_code=status.HTTP_200_OK
)
async def get_city(response: Response, id_city: int, db: Session = Depends(database.get_data_base)):
    cities = get_city_by_id(id_city, db)

    if cities is None:
        await _throwerExceptions.throw_custom_exception(name=Constants.CITIES_NOT_FOUND_ERROR,
                                                        detail=Constants.CITIES_NOT_FOUND_ERROR,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return cities


@territory_controller.get(
    '/cities/{id_city}/states',
    status_code=status.HTTP_200_OK
)
async def get_states_by_city(response: Response, id_city: int, db: Session = Depends(database.get_data_base)):
    states = get_states(id_city, db)

    if len(states) == 0:
        await _throwerExceptions.throw_custom_exception(name=Constants.STATES_NOT_FOUND_ERROR,
                                                        detail=Constants.STATES_NOT_FOUND_ERROR,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return states


@territory_controller.get(
    '/state/{id_state}',
    status_code=status.HTTP_200_OK
)
async def get_state(response: Response, id_state: int, db: Session = Depends(database.get_data_base)):
    state = get_state_by_id(id_state, db)

    if state is None:
        await _throwerExceptions.throw_custom_exception(name=Constants.STATES_NOT_FOUND_ERROR,
                                                        detail=Constants.STATES_NOT_FOUND_ERROR,
                                                        status_code=status.HTTP_204_NO_CONTENT)

    return state
