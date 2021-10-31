from fastapi import status
from loguru import logger
from validator.SearchValidator import SearchValidator
from repository.dao.SearchDao import SearchDAO
from configuration.database.database import SessionLocal
from exception.exceptions import CustomError
from dto.request.search_request_dto import SearchParameter


class SearchService:
    SORT_BY = {1: "rating", 2: "name", 3: "price"}
    ORDER_BY = {1: "asc", 2: "desc"}
    MSG_ERROR_MS_LOCAL = "Error al buscar locales"
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
            self.raise_custom_error(name=self.MSG_ERROR_MS_LOCAL, message=all_branches)

        return SearchParameter.to_search_branches_response(content=all_branches)

    async def search_branch_profile(self, branch_id: int):
        logger.info('branch_id: {}', branch_id)
        #search_dto = SearchDTO()
        #ms_local_client = MSLocalClient()
        #branch_profile = await ms_local_client.search_branch_profile(branch_id=branch_id)

        #if type(branch_profile) == str:
        #    search_dto.error = self.NOT_BRANCH_MSG_ERROR
        #    return search_dto.__dict__

        #search_dto.data = branch_profile
        #return search_dto.__dict__

    def clear_null_values(self, values: dict):
        logger.info('values: {}', values)
        clean_values = {}
        for key, element in values.items():
            clean_values[key] = element if element != 'null' else None

        logger.info('clean_values: {}', clean_values)
        return clean_values

    def get_branch(self, branch_id: int, db: SessionLocal):
        logger.info('branch_id: {}', branch_id)
        attribute_dict = self.read_branch(branch_id=branch_id, db=db)

        if type(attribute_dict) == list:
            return self.create_response(data=attribute_dict)

        if type(attribute_dict) != dict:
            return self.create_response(data=attribute_dict)

        branch = self.populate_branch_profile(attribute_dict=attribute_dict)
        return self.create_response(branch)

    def populate_branch_profile(self, attribute_dict: dict):
        logger.info('attribute_dict: {}', attribute_dict)
        attribute = {
            'id': attribute_dict['branch']['id'],
            'name': attribute_dict['branch']['name'],
            'description': attribute_dict['branch']['description'],
            'latitude': attribute_dict['branch']['latitude'],
            'longitude': attribute_dict['branch']['longitude'],
            'accept_pet': attribute_dict['branch']['accept_pet'],
            'street': attribute_dict['branch']['street'],
            'street_number': attribute_dict['branch']['street_number'],
            'rating': attribute_dict['aggregate_values']['rating'] if attribute_dict['aggregate_values'] else 0,
            'price': attribute_dict['aggregate_values']['price'] if attribute_dict['aggregate_values'] else 0,
            'min_price': attribute_dict['aggregate_values']['min_price'] if attribute_dict['aggregate_values'] else 0,
            'max_price': attribute_dict['aggregate_values']['max_price'] if attribute_dict['aggregate_values'] else 0,
            'related_branch': attribute_dict['related_branch'],
            'branch_images': attribute_dict['branch_images'],
            'opinion_list': attribute_dict['opinion_list'],
            'schedule_list': attribute_dict['schedule_branch']
        }
        logger.info('attribute: {}', attribute)
        return attribute

    def raise_custom_error(self, name: str, message: str):
        raise CustomError(name=name,
                          detail=message,
                          status_code=status.HTTP_400_BAD_REQUEST,
                          cause="")  # TODO: Llenar campo
