from datetime import datetime
from loguru import logger
from schema.search_schema import SearchParameters
from validator.search_validator import validate_search_paramters
from dto.dto import GenericDTO as SearchDTO
from integration.integrations import MSLocalClient

MSG_ERROR_MS_LOCAL = "Error al buscar locales" # TODO: Mejorar todas las respuesta, más descriptivas
LIMIT_HOUR_MSG_ERROR = "No es posible realizar petición en horario toque de queda"
LIMIT_HOUR = 22

async def search_all_branch(search_parameters: SearchParameters, client_id: int = None):
    logger.info('search_paramters: {}', search_parameters)
    validated_data = validate_search_paramters(search_parameters=search_parameters)
    # TODO: Validar si la request es igual o después de las 22:00hrs devolver error por toque de queda.
    search_dto = SearchDTO()

    if validated_data:
        logger.error('validated_data: {}', validated_data)
        search_dto.error = validated_data
        return search_dto.__dict__

    if datetime.now().time().hour >= LIMIT_HOUR:
        logger.error('Request realizado en toque de queda')
        search_dto.error = LIMIT_HOUR_MSG_ERROR
        return search_dto.__dict__

    if search_parameters.date_reservation:
        search_parameters.date_reservation = search_parameters.date_reservation.replace("/", "-") + " 00:00:00"  # TODO: Hora por definir

    print(dict(search_parameters))

    ms_local_client = MSLocalClient()
    all_branch = await ms_local_client.search_all_branch(search_parameters=dict(search_parameters), client_id=client_id)
    logger.info('all_branch: {}', all_branch)

    if type(all_branch) != list:  # SI hay data o es válida, siepmre será una lista
        search_dto.error = MSG_ERROR_MS_LOCAL
        return search_dto.__dict__

    search_dto.data = all_branch
    return search_dto.__dict__


