import re
from loguru import logger
from schema.search_schema import SearchParameters
from dateutil.parser import parse

STRING_REGEX = re.compile(r"[A-Za-z\sáéíóúÁÉÍÓÚñ]+")
SORT_BY_INDEX_LIST = [1, 2, 3, 4, 5]
ORDER_BY_INDEX_LIST = [1, 2]
DATE_RESERVATION_REGEX = re.compile(r"2[0-9]{3}/[0-9]{2}/[0-9]{2}")
# TODO: Poner constantes para validar date_reservation por año  mes y día
INVALID_DATA_MESSAGE = "Formato no válido"  # TODO: Podría ser general, en ingles y toda validacion en un solo archivo?


def validate_search_paramters(search_parameters: SearchParameters):
    logger.info('search_parameters:{}', search_parameters)
    data_checked = {}

    if search_parameters.name and not re.fullmatch(STRING_REGEX, search_parameters.name):
        data_checked['name'] = INVALID_DATA_MESSAGE

    if search_parameters.state_id and type(search_parameters.state_id) != int:  # TODO: Falta agregar rando de IDs
        data_checked['state_id'] = INVALID_DATA_MESSAGE

    if search_parameters.date_reservation and not re.fullmatch(DATE_RESERVATION_REGEX, search_parameters.date_reservation):
        data_checked['date_reservation'] = INVALID_DATA_MESSAGE
    if search_parameters.sort_by and (type(search_parameters.sort_by) != int or search_parameters.sort_by not in SORT_BY_INDEX_LIST):
        data_checked['sort_by'] = INVALID_DATA_MESSAGE

    if search_parameters.order_by and (type(search_parameters.order_by) != int or search_parameters.order_by not in ORDER_BY_INDEX_LIST):
        data_checked['order_by'] = INVALID_DATA_MESSAGE

    return data_checked

