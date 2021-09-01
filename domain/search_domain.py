from fastapi import status
import json
from datetime import datetime
from loguru import logger
from schema.search_schema import SearchParameters
from validator.search_validator import validate_search_paramters
from dto.dto import GenericDTO as SearchDTO
from integration.integrations import MSLocalClient, MSIntegrationApi

MSG_ERROR_MS_LOCAL = "Error al buscar locales" # TODO: Mejorar todas las respuesta, más descriptivas
LIMIT_HOUR_MSG_ERROR = "No es posible realizar petición después de estar a dos horas o menos de toque de queda"
LIMIT_HOUR = 22
MSG_UNAUTHORIZED = "Usuario no autorizado"
# TODO: Se debe refactorizar lo siguiente:
# TODO: - Manejar status code en capa domain junto con el json_load de la response. Capa integration solo se comunica y devuelve la respuesta cruda

async def search_all_branch(search_parameters: SearchParameters, client_id: int = None, client_token: str = None):
    logger.info('search_paramters: {}, client_id: {}', search_parameters, client_id)
    search_dto = SearchDTO()

    validated_data = {}

    if search_parameters != {}:
        validated_data = validate_search_paramters(search_parameters=search_parameters)

    if validated_data:
        logger.error('validated_data: {}', validated_data)
        search_dto.error = validated_data
        return search_dto.__dict__

    if datetime.now().time().hour >= LIMIT_HOUR:
        logger.error('Request realizado en toque de queda')
        search_dto.error = LIMIT_HOUR_MSG_ERROR
        return search_dto.__dict__

    if search_parameters != {} and search_parameters.date_reservation:
        search_parameters.date_reservation = search_parameters.date_reservation.replace("/", "-")

    ms_local_client = MSLocalClient()
    all_branch = await ms_local_client.search_all_branch(search_parameters=dict(search_parameters), client_id=client_id)
    logger.info('all_branch: {}', all_branch)

    if type(all_branch) != list:  # SI hay data o es válida, siepmre será una lista
        search_dto.error = MSG_ERROR_MS_LOCAL
        return search_dto.__dict__

    search_dto.data = all_branch
    return search_dto.__dict__


async def validate_token(client_token: str):
    search_dto = SearchDTO()
    ms_integration_api = MSIntegrationApi()

    response = await ms_integration_api.validate_token(client_token=client_token)
    validated_token = json.loads(response.text) # TODO: Parece que devuelve true si es correcto. Agregar a validacion
    if response.status_code != status.HTTP_200_OK:
        search_dto.error = MSG_UNAUTHORIZED

    return search_dto.__dict__
