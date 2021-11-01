from fastapi import status
from loguru import logger
from validator.SearchValidator import SearchValidator
from repository.dao.SearchDao import SearchDAO
from configuration.database.database import SessionLocal
from exception.exceptions import CustomError
from dto.request.search_request_dto import SearchParameter
from dto.dto import GenericDTO as wrapperDTO


class SearchService:
    SORT_BY = {1: "rating", 2: "name", 3: "price"}
    ORDER_BY = {1: "asc", 2: "desc"}
    MSG_ERROR_ALL_BRANCHES = "Error al buscar locales"
    MSG_ERROR_BRANCH_PROFILE = "Error al obtener perfil local"
    NOT_BRANCH_MSG_ERROR = "Error, local no existente"
    NOT_BRANCH_RAW_MSG_ERROR = "'NoneType' object has no attribute 'restaurant_id'"
    search_validator = SearchValidator()
    search_dao = SearchDAO()

    async def search_all_branches(self, parameters: SearchParameter, db: SessionLocal, client_id: int):
        logger.info('parameters: {}, client_id: {}', parameters, client_id)

        search_parameters = self.clear_null_values(values=parameters)  # TODO: Formato datetime validar con otra función y no con REGEX

        self.search_validator.validate_search_parameters(search_parameters=search_parameters)

        if search_parameters['date_reservation']:
            search_parameters['date_reservation'] = search_parameters['date_reservation'].replace("/", "-")
            logger.info('search_parameters[date_reservation]: {}', search_parameters['date_reservation'])

        all_branches = self.search_dao\
            .search_all_branches(search_parameters=search_parameters, client_id=client_id, db=db)

        if type(all_branches) is str:
            self.raise_custom_error(name=self.MSG_ERROR_ALL_BRANCHES, message=all_branches)

        return SearchParameter.to_search_branches_response(content=all_branches)

    async def search_branch_profile(self, branch_id: int, client_id: int, db: SessionLocal):
        logger.info('branch_id: {}', branch_id)
        branch_dict = self.search_dao.search_branch_profile(branch_id=branch_id, client_id=client_id, db=db)

        if type(branch_dict) is str:
            self.raise_custom_error(name=self.MSG_ERROR_BRANCH_PROFILE, message=branch_dict)

        branch_profile_populated = self.populate_branch_profile(branch_dict=branch_dict)
        return self.to_branch_profile_response(content=branch_profile_populated)

    def clear_null_values(self, values: dict):
        logger.info('values: {}', values)
        clean_values = {}
        for key, element in values.items():
            clean_values[key] = element if element != 'null' else None

        logger.info('clean_values: {}', clean_values)
        return clean_values

    def populate_branch_profile(self, branch_dict: dict):
        logger.info('branch_dict: {}', branch_dict)
        branch_profile = {
            'id': branch_dict['branch']['id'],
            'description': branch_dict['branch']['description'],
            'latitude': branch_dict['branch']['latitude'],
            'longitude': branch_dict['branch']['longitude'],
            'street': branch_dict['branch']['street'],
            'street_number': branch_dict['branch']['street_number'],
            'accept_pet': branch_dict['branch']['accept_pet'],
            'name': branch_dict['branch']['name'],
            'state_name': branch_dict['branch']['state_name'],
            'rating': branch_dict['aggregate_values']['rating'] if branch_dict['aggregate_values'] else 0,
            'avg_price': branch_dict['aggregate_values']['avg_price'] if branch_dict['aggregate_values'] else 0,
            'min_price': branch_dict['aggregate_values']['min_price'] if branch_dict['aggregate_values'] else 0,
            'max_price': branch_dict['aggregate_values']['max_price'] if branch_dict['aggregate_values'] else 0,
            'branches': branch_dict['branches'],
            'images': branch_dict['images'],
            'schedule': branch_dict['schedule'],
            'opinions': branch_dict['opinions']
        }
        logger.info('branch_profile: {}', branch_profile)
        return branch_profile

    def raise_custom_error(self, name: str, message: str):
        raise CustomError(name=name,
                          detail=message,
                          status_code=status.HTTP_400_BAD_REQUEST,
                          cause="")  # TODO: Llenar campo

    def to_branch_profile_response(self, content):  # TODO: Mover función a otra clase(?)
        response = wrapperDTO()
        response.data = content
        return response.__dict__
