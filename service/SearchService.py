from loguru import logger
from validator.SearchValidator import SearchValidator
from repository.dao.SearchDAO import SearchDAO
from configuration.database.database import SessionLocal

class SearchService:
    SORT_BY = {1: "rating", 2: "name", 3: "price"}
    ORDER_BY = {1: "asc", 2: "desc"}
    MSG_ERROR_MS_LOCAL = "Error al buscar locales"  # TODO: Mejorar todas las respuesta, más descriptivas
    NOT_BRANCH_MSG_ERROR = "Error, local no existente"
    NOT_BRANCH_RAW_MSG_ERROR = "'NoneType' object has no attribute 'restaurant_id'"
    search_validator = SearchValidator()
    search_dao = SearchDAO()

    # TODO: Ver si funcion __call__ sirve o algo propio de python class
    async def search_all_branches(self, parameters: dict, client_id: int = None):
        logger.info('parameters: {}, client_id: {}', parameters, client_id)

        search_parameters = self.clear_null_values(values=parameters)

        self.search_validator.validate_search_parameters(search_parameters=search_parameters)

        if search_parameters['date_reservation']:
            search_parameters['date_reservation'] = search_parameters['date_reservation'].replace("/", "-")
            logger.info('search_parameters[date_reservation]: {}', search_parameters['date_reservation'])

        # TODO: Preparar query según parámetros entrantes
        # TODO: Enviar query hacia SearchDAO
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
        return clean_values # -------------------------------------------------- #

    def define_raw_query(self, parameters: dict, client_id: int):  # TODO: Se debe optimizar la query y clausula WITH
        query_parameters = self.define_with_clause_query(parameters=parameters)

        is_favourite_query = ", COALESCE ((SELECT f.is_favourite " \
                             f"FROM tyne.favourite f WHERE f.branch_id = b.id AND f.client_id = {client_id}), false) " \
                             "AS is_favourite " if client_id else ''
        base_query = "SELECT " \
                     "b.id, " \
                     "pb.name AS name, " \
                     "b.description, " \
                     "AVG(o.qualification) AS rating, " \
                     "AVG(pr.amount)::int AS price, " \
                     "MIN(pr.amount)::int AS min_price, " \
                     "MAX(pr.amount)::int AS max_price, " \
                     "(SELECT i.url " \
                     "FROM tyne.branch_image bi JOIN tyne.image i ON bi.image_id = i.id " \
                     "WHERE bi.branch_id = b.id ORDER BY i.id ASC LIMIT 1) " \
                     "AS image_url " \
                     f"{is_favourite_query}" \
                     "FROM " \
                     "preview_branch pb " \
                     "LEFT JOIN " \
                     "tyne.branch b " \
                     "ON pb.id = b.id " \
                     "LEFT JOIN " \
                     "tyne.opinion o " \
                     "ON b.id = o.branch_id " \
                     "LEFT JOIN " \
                     "tyne.product p " \
                     "ON b.id = p.branch_id " \
                     "LEFT JOIN " \
                     "tyne.price pr " \
                     "ON p.id = pr.product_id " \
                     "WHERE " \
                     "pb.reservation_count < 4 AND b.state = true " \
                     "GROUP BY " \
                     "b.id, pb.name" \
                     f"{query_parameters['order']};"

        with_clause = 'WITH preview_branch AS ( ' \
                      'SELECT ' \
                      'b.id, ' \
                      'rt.name, ' \
                      f"{query_parameters['reservation_query']} AS reservation_count " \
                      'FROM ' \
                      'tyne.branch b ' \
                      'LEFT JOIN ' \
                      'tyne.restaurant rt ' \
                      'ON b.restaurant_id = rt.id ' \
                      'LEFT JOIN ' \
                      'tyne.reservation r ' \
                      'ON b.id = r.branch_id ' \
                      f"{query_parameters['where']}" \
                      f"{query_parameters['name']}" \
                      f"{query_parameters['and']}" \
                      f"{query_parameters['state_id']}" \
                      'GROUP BY ' \
                      'b.id, rt.id ' \
                      ') '
        full_raw_query = with_clause + base_query
        logger.info('full_raw_query: {}', full_raw_query)
        return full_raw_query

    def define_with_clause_query(self, parameters: dict):
        query_parameters = {
            'where': 'WHERE ' if parameters['name'] or parameters['state_id'] else '',
            'name': f"LOWER(rt.name) LIKE LOWER('%{parameters['name']}%') " if parameters['name'] else '',
            'and': 'AND ' if parameters['name'] and parameters['state_id'] else '',
            'state_id': f"b.state_id = {parameters['state_id']} " if parameters['state_id'] else '',
            'reservation_query': 0,
            'order': f" ORDER BY {self.SORT_BY[parameters['sort_by']]} " if parameters['sort_by'] else ''
        }

        if query_parameters['order'] != '' and parameters['order_by']:
            query_parameters['order'] += self.ORDER_BY[parameters['order_by']]

        if parameters['date_reservation']:
            query_parameters['reservation_query'] = "COUNT(r.id) FILTER (WHERE r.reservation_date = " \
                                                    f"'{parameters['date_reservation']}')"
        if parameters['order_by']:  # TODO: Por definir
            pass

        logger.info('query_parameters: {}', query_parameters)
        return query_parameters

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

    def create_response(data):
        logger.info('Data: {}', data)
        local_dto = {
            'data': None,
            'error': None
        }

        if type(data) != str:  # TODO: Definir bien estructura de respuesta
            local_dto.data = data

        else:
            local_dto.error = data

        return local_dto.__dict__


