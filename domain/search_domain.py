from fastapi import status
import json
from datetime import datetime
from loguru import logger
from schema.search_schema import SearchParameters
from validator.search_validator import validate_search_parameters
from dto.dto import GenericDTO as SearchDTO
from integration.integrations import MSLocalClient, MSIntegrationApi

MSG_ERROR_MS_LOCAL = "Error al buscar locales" # TODO: Mejorar todas las respuesta, más descriptivas
LIMIT_HOUR_MSG_ERROR = "No es posible realizar petición después de estar a dos horas o menos de toque de queda"
LIMIT_HOUR = 22

# TODO: Se debe refactorizar lo siguiente:
# TODO: Manejar status code en capa domain junto con json_load de response.
# TODO: Capa integration solo comunica y devuelve respuesta cruda


async def search_all_branch(parameters: dict, client_id: int = None):
    logger.info('parameters: {}, client_id: {}', parameters, client_id)
    search_dto = SearchDTO()

    search_parameters = clear_null_values(values=parameters)

    validated_data = {}

    validated_data = validate_search_parameters(search_parameters=search_parameters)

    if validated_data:
        logger.error('validated_data: {}', validated_data)
        search_dto.error = validated_data
        return search_dto.__dict__
    '''
    if datetime.now().time().hour >= LIMIT_HOUR:
        logger.error('Request realizado en toque de queda')
        search_dto.error = LIMIT_HOUR_MSG_ERROR
        return search_dto.__dict__
    '''
    if search_parameters['date_reservation']:
        search_parameters['date_reservation'] = search_parameters['date_reservation'].replace("/", "-")

    query_parameters = define_query_parameters(search_parameters=search_parameters)

    ms_local_client = MSLocalClient()
    all_branch = await ms_local_client.search_all_branch(query_parameters=query_parameters, client_id=client_id)
    logger.info('all_branch: {}', all_branch)

    if type(all_branch) != list:  # SI hay data o es válida, siepmre será una lista
        search_dto.error = MSG_ERROR_MS_LOCAL
        return search_dto.__dict__

    search_dto.data = all_branch
    return search_dto.__dict__


def define_query_parameters(search_parameters: dict):

    query_parameters = '?'
    for key, element in search_parameters.items():
        query_parameters += f"{key}={element}&" if search_parameters[key] else ''

    if query_parameters != '?':
        query_parameters = query_parameters[:-1]

    logger.info('query_parameters: {}', query_parameters)

    return query_parameters


async def search_branch_profile(branch_id: int):
    logger.info('branch_id: {}', branch_id)
    search_dto = SearchDTO()
    ms_local_client = MSLocalClient()
    branch_profile = await ms_local_client.search_branch_profile(branch_id=branch_id)

    if type(branch_profile) == str:
        search_dto.error = branch_profile

    search_dto.data = branch_profile
    return search_dto.__dict__


def clear_null_values(values: dict):
    logger.info('values: {}', values)
    clean_values = {}
    for key, element in values.items():

        clean_values[key] = element if element != 'null' else None

    logger.info('clean_values: {}', clean_values)

    return clean_values
