from loguru import logger
from dto.request.local_request_dto import NewAccount, NewBranch
from validator.LocalValidator import LocalValidator
from exception.exceptions import CustomError
from fastapi import status
from service.MapboxService import MapBoxService
from service.FirebaseService import FirebaseService
from repository.dao.LocalDAO import LocalDAO
from dto.request.local_request_dto import ParserDTO
from configuration.database.database import SessionLocal


class LocalService:
    MSG_CREATE_ACCOUNT_SUCCESSFULLY = "Local creado correctamente"
    MSG_ERROR_BRANCH_ADDRESS = "Dirección de local no válida"
    LEGAL_REPRESENTATIVE_KEY_WORD = 'legal_representative_identifier_key'
    LEGAL_REPRESENTATIVE_ERROR_MESSAGE = 'Rut representante legal ya está registrado'
    RESTAURANT_KEY_WORD = 'restaurant_identifier_key'
    RESTAURANT_ERROR_MESSAGE = 'Rut restaurant ya está registrado'
    STANDARD_ERROR_MESSAGE = 'Error en base de datos'
    CREATE_ACCOUNT_ERROR_MSG = 'Error al registrar cuenta de local'
    GET_PROFILE_ERROR_MSG = 'Error al obtener perfil sucursal'
    NEW_BRANCH_ERROR_MSG = 'Error al agregar una sucursal nueva'
    EMAIL_KEY_WORD = 'email'
    EMAIL_ERROR_MESSAGE = 'Email de usuario ya está registrado'
    MSG_NEW_BRANCH = 'Sucursal agregado correctamente'
    ID_USER_TYPE = 1
    parser_dto = ParserDTO()

    async def create_new_account(self, new_account: NewAccount, db: SessionLocal):
        logger.info('new_account: {}', new_account)

        local_validator = LocalValidator()
        local_validator.validate_new_account(new_account=new_account)

        branch = new_account.branch
        logger.info('branch: {}', branch)
        branch_geocoding = await self.geocoding(street=branch.street, street_number=branch.street_number)
        logger.info('branch_geocoding: {}', branch_geocoding)

        manager = new_account.manager
        logger.info('manager: {}', manager)

        user = {'email': manager.email, 'password': manager.password}
        logger.info('user: {}', user)
        user_entity = new_account.to_user_entity(user_dict=user, id_user_type=self.ID_USER_TYPE)
        logger.info('user_entity: {}', user_entity)

        manager_entity = new_account.to_manager_entity(manager=manager)
        logger.info('manager_entity: {}', manager_entity)

        legal_representative = new_account.legal_representative
        logger.info('legal_representative: {}', legal_representative)
        legal_representative_entity = new_account.\
            to_legal_representative_entity(legal_representative=legal_representative)

        restaurant = new_account.restaurant
        logger.info('restaurant: {}', restaurant)
        restaurant_entity = new_account.to_restaurant_entity(restaurant=restaurant, name=branch.name)

        branch_entity = new_account.to_branch_entity(branch=branch, branch_geocoding=branch_geocoding)
        logger.info('branch_entity: {}', branch_entity)

        branch_bank = new_account.branch_bank
        logger.info('branch_bank: {}', branch_bank)
        branch_bank_entity = new_account.to_branch_bank_entity(branch_bank=branch_bank)

        local_dao = LocalDAO()
        branch_entity_status = local_dao.register_account(user_entity=user_entity,
                                                          manager_entity=manager_entity,
                                                          legal_representative_entity=legal_representative_entity,
                                                          restaurant_entity=restaurant_entity,
                                                          branch_entity=branch_entity,
                                                          branch_bank_entity=branch_bank_entity,
                                                          db=db)

        logger.info('branch_entity_status: {}', branch_entity_status)

        if type(branch_entity_status) is str:
            branch_entity_status_parsed = self.parse_error_response_database(message=branch_entity_status)
            self.raise_custom_error(name=self.CREATE_ACCOUNT_ERROR_MSG, message=branch_entity_status_parsed)

        return new_account.to_branch_create_response(content=self.MSG_CREATE_ACCOUNT_SUCCESSFULLY)

    async def geocoding(self, street: str, street_number: int):
        logger.info('street: {}, street_number: {}', street, street_number)
        mapbox_service = MapBoxService()

        address = street + " " + str(street_number)
        logger.info('address: {}', address)

        coordinates = await mapbox_service.get_latitude_longitude(address=address)
        logger.info("coordinates: {}", coordinates)
        return coordinates

    async def create_credentials(self, email: str, password: str):
        logger.info('email: {}, password: {}', email, password)
        firebase_service = FirebaseService()
        uid = await firebase_service.create_account(email=email, password=password)
        return uid

    async def delete_credentials(self, uid):
        logger.info('uid: {},', uid)
        firebase_service = FirebaseService()
        await firebase_service.delete_account(uid=uid)
        pass

    def get_account_profile(self, branch_id: int, db: SessionLocal):
        logger.info('branch_id: {}', branch_id)

        local_dao = LocalDAO()
        branch_profile = local_dao.get_account_profile(branch_id=branch_id, db=db)

        if type(branch_profile) is str:
            logger.error("branch_profile: {}", branch_profile)
            self.raise_custom_error(name=self.GET_PROFILE_ERROR_MSG, message=branch_profile)

        return self.parser_dto.to_branch_create_response(content=branch_profile)

    async def add_new_branch(self, branch_id, new_branch: NewBranch, db: SessionLocal):
        logger.info('branch_id: {}', branch_id)
        local_validator = LocalValidator()
        local_validator.validate_new_branch(new_branch=new_branch)

        branch = new_branch.branch
        logger.info('branch: {}', branch)
        branch_geocoding = await self.geocoding(street=branch.street, street_number=branch.street_number)
        logger.info('branch_geocoding: {}', branch_geocoding)

        manager = new_branch.manager
        logger.info('manager: {}', manager)

        user = {'email': manager.email, 'password': manager.password}
        logger.info('user: {}', user)
        user_entity = new_branch.to_user_entity(user_dict=user, id_user_type=self.ID_USER_TYPE)
        logger.info('user_entity: {}', user_entity)

        manager_entity = new_branch.to_manager_entity(manager=manager)

        branch_entity = new_branch.to_branch_entity(branch=branch,
                                                    branch_geocoding=branch_geocoding)
        branch_bank = new_branch.branch_bank
        branch_bank_entity = new_branch.to_branch_bank_entity(branch_bank=branch_bank)

        local_dao = LocalDAO()
        new_branch_status = local_dao.add_new_branch(user_entity=user_entity,
                                                     branch_id=branch_id,
                                                     manager_entity=manager_entity,
                                                     branch_entity=branch_entity,
                                                     branch_bank_entity=branch_bank_entity,
                                                     db=db)

        logger.info('new_branch_status: {}', new_branch_status)

        if type(new_branch_status) is str:
            new_branch_status_parsed = self.parse_error_response_database(message=new_branch_status)
            self.raise_custom_error(name=self.NEW_BRANCH_ERROR_MSG, message=new_branch_status_parsed)

        return new_branch.to_branch_create_response(content=self.MSG_NEW_BRANCH)

    def raise_custom_error(self, name: str, message: str):   # TODO: Esta función debe ser de otra clase creo.
        raise CustomError(name=name,
                          detail=message,
                          status_code=status.HTTP_400_BAD_REQUEST if message else status.HTTP_204_NO_CONTENT,
                          cause="")  # TODO: Llenar campo

    def parse_error_response_database(self, message):

        if self.LEGAL_REPRESENTATIVE_KEY_WORD in message:
            return self.LEGAL_REPRESENTATIVE_ERROR_MESSAGE

        if self.RESTAURANT_KEY_WORD in message:
            return self.RESTAURANT_ERROR_MESSAGE

        if self.EMAIL_KEY_WORD in message:
            return self.EMAIL_ERROR_MESSAGE
        return self.STANDARD_ERROR_MESSAGE
