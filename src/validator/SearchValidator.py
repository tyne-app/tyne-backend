import re

from fastapi import status
from loguru import logger

from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions


class SearchValidator:
    STRING_REGEX = re.compile(r"[A-Za-z0-9\sáéíóúÁÉÍÓÚñ]+")
    SORT_BY_INDEX_LIST = [1, 2, 3]
    ORDER_BY_INDEX_LIST = [1, 2]
    DATE_RESERVATION_REGEX = re.compile(r"2[0-9]{3}/[0-9]{2}/[0-9]{2}")
    # TODO: Poner constantes para validar date_reservation por año  mes y día
    INVALID_DATA_MESSAGE = "Valor no válido"  # TODO: Podría ser general, en ingles y toda validacion en un solo archivo?
    _throwerExceptions = ThrowerExceptions()

    async def validate_search_parameters(self, search_parameters: dict):
        logger.info('search_parameters:{}', search_parameters)

        data_checked = {}

        if search_parameters['name'] and not re.fullmatch(self.STRING_REGEX, search_parameters['name']):
            data_checked['name'] = self.INVALID_DATA_MESSAGE

        if search_parameters['state_id'] and type(search_parameters['state_id']) != int:  # TODO: Falta agregar rango de IDs
            data_checked['state_id'] = self.INVALID_DATA_MESSAGE

        if search_parameters['date_reservation'] and not re.fullmatch(self.DATE_RESERVATION_REGEX, search_parameters['date_reservation']):
            data_checked['date_reservation'] = self.INVALID_DATA_MESSAGE

        if search_parameters['sort_by'] and (type(search_parameters['sort_by']) != int or search_parameters['sort_by'] not in self.SORT_BY_INDEX_LIST):
            data_checked['sort_by'] = self.INVALID_DATA_MESSAGE

        if search_parameters['order_by'] and (type(search_parameters['order_by']) != int or search_parameters['order_by'] not in self.ORDER_BY_INDEX_LIST):
            data_checked['order_by'] = self.INVALID_DATA_MESSAGE

        if data_checked:
            logger.error("data_checked: {}", data_checked)
            await self._throwerExceptions.throw_custom_exception(name=Constants.FIELDS_VALIDATOR_ERROR,
                                                                 detail=data_checked,
                                                                 status_code=status.HTTP_400_BAD_REQUEST,
                                                                 cause=data_checked)
