from loguru import logger
from schema.search_schema import SearchParameters
from validator.search_validator import validate_search_paramters
from dto.dto import GenericDTO as SearchDTO


def search_all_branch(search_parameters: SearchParameters):
    logger.info('search_paramters: {}', search_parameters)
    validated_data = validate_search_paramters(search_parameters=search_parameters)

    if validated_data:
        logger.info('validated_data: {}', validated_data)
        search_dto = SearchDTO()
        search_dto.error = validated_data
        return search_dto.__dict__

    if search_parameters.date_reservation:
        search_parameters.date_reservation = search_parameters.date_reservation.replace("/", "-")

    print(dict(search_parameters))

    return {}


