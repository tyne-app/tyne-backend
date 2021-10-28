from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from configuration.database import database
from dto.response.GenericResponse import create_response
from repository.dao.CityDao import get_cities, get_city_by_id
from repository.dao.CountryDao import get_all_countries, get_country_by_id
from repository.dao.StateDao import get_states, get_state_by_id

territory_controller = APIRouter(
    prefix="/v1/territories",
    tags=["Territories"]
)


@territory_controller.get(
    '/countries',
    status_code=status.HTTP_200_OK
)
def get_countries(response: Response, db: Session = Depends(database.get_data_base)):
    data = get_all_countries(db)

    if len(data) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)


@territory_controller.get(
    '/countries/{id_country}',
    status_code=status.HTTP_200_OK
)
def get_country(response: Response, id_country: int, db: Session = Depends(database.get_data_base)):
    data = get_country_by_id(id_country, db)

    if data is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)


@territory_controller.get(
    '/countries/{id_country}/cities',
    status_code=status.HTTP_200_OK
)
def get_cities_by_country(response: Response, id_country: int, db: Session = Depends(database.get_data_base)):
    data = get_cities(id_country, db)

    if len(data) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)


@territory_controller.get(
    '/cities/{id_city}',
    status_code=status.HTTP_200_OK
)
def get_city(response: Response, id_city: int, db: Session = Depends(database.get_data_base)):
    data = get_city_by_id(id_city, db)

    if data is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)


@territory_controller.get(
    '/cities/{id_city}/states',
    status_code=status.HTTP_200_OK
)
def get_states_by_city(response: Response, id_city: int, db: Session = Depends(database.get_data_base)):
    data = get_states(id_city, db)

    if len(data) == 0:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)


@territory_controller.get(
    '/state/{id_state}',
    status_code=status.HTTP_200_OK
)
def get_state(response: Response, id_state: int, db: Session = Depends(database.get_data_base)):
    data = get_state_by_id(id_state, db)

    if data is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return create_response(data)
