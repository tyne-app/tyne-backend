from loguru import logger
from dto.request.local_request_dto import NewAccount
from validator.LocalValidator import LocalValidator
from exception.exceptions import CustomError
from fastapi import APIRouter, Depends, Response, status
from service.MapboxService import MapBoxService
from service.FirebaseService import FirebaseService
from repository.dao.LocalDAO import LocalDAO
from mappers.request.BranchBankMapperRequest import BranchBankMapperRequest
from mappers.request.ManagerMapperRequest import ManagerMapperRequest
from mappers.request.LegalRepresentativeMapperRequest import LegalRepresentativeMapperRequest
from mappers.request.RestaurantMapperRequest import RestaurantMapperRequest
from mappers.request.BranchMapperRequest import BranchMapperRequest
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchBankEntity import BranchBankEntity
from configuration.database.database import SessionLocal


class LocalService:

    MSG_ERROR_BRANCH_ADDRESS = "Dirección de local no válida"
    LEGAL_REPRESENTATIVE_KEY_WORD = 'legal_representative_identifier_key'
    LEGAL_REPRESENTATIVE_ERROR_MESSAGE = 'Rut representante legal ya está registrado'
    RESTAURANT_KEY_WORD = 'restaurant_identifier_key'
    RESTAURANT_ERROR_MESSAGE = 'Rut restaurant ya está registrado'
    STANDARD_ERROR_MESSAGE = 'Error en base de datos'

    async def create_new_account(self, new_account: NewAccount, db: SessionLocal):
        logger.info('new_account: {}', new_account)

        local_validator = LocalValidator()
        validated_data = local_validator.validate_new_account(new_account=new_account)

        if validated_data:
            logger.error("validated_data: {}", validated_data)
            self.raise_custom_error(message=validated_data)

        branch = new_account.branch
        logger.info('branch: {}', branch)
        branch_geocoding = await self.geocoding(street=branch.street, street_number=branch.street_number)
        logger.info('branch_geocoding: {}', branch_geocoding)

        manager = new_account.manager
        logger.info('manager: {}', manager)
        uid = await self.create_credentials(email=manager.email, password=manager.password)
        logger.info('uid: {}', uid)

        manager_mapper_request = ManagerMapperRequest()
        manager_entity = manager_mapper_request.to_manager_entity(manager=manager)

        legal_representative = new_account.legal_representative
        legal_representative_mapper_request = LegalRepresentativeMapperRequest()
        legal_representative_entity = legal_representative_mapper_request. \
            to_legal_representative_entity(legal_representative=legal_representative)

        restaurant = new_account.restaurant
        restaurant_mapper_request = RestaurantMapperRequest()
        restaurant_entity = restaurant_mapper_request.to_restaurant_entity(restaurant=restaurant, name=branch.name)

        branch_mapper_request = BranchMapperRequest()
        branch_entity = branch_mapper_request.to_branch_entity(branch=branch, branch_geocoding=branch_geocoding,
                                                               uid=uid)  # TODO: Verificar UID de firebaseService

        branch_bank = new_account.branch_bank
        branch_bank_mapper_request = BranchBankMapperRequest()
        branch_bank_entity = branch_bank_mapper_request.to_branch_bank_entity(branch_bank=branch_bank)

        # TODO: Definir cómo manejar respuesta
        branch_entity_status = self.persist_new_account(uid=uid,
                                                              manager_entity=manager_entity,
                                                              legal_representative_entity=legal_representative_entity,
                                                              restaurant_entity=restaurant_entity,
                                                              branch_entity=branch_entity,
                                                              branch_bank_entity=branch_bank_entity,
                                                              db=db)
        logger.info('branch_entity_status: {}', branch_entity_status)

        if type(branch_entity_status) is str:
            await self.delete_credentials(uid=uid)
            self.raise_custom_error(message=branch_entity_status)

        return branch_mapper_request.to_branch_create_response()

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

    def persist_new_account(self,
                                  uid: str,
                                  manager_entity: ManagerEntity,
                                  legal_representative_entity: LegalRepresentativeEntity,
                                  restaurant_entity: RestaurantEntity,
                                  branch_entity: BranchEntity,
                                  branch_bank_entity: BranchBankEntity,
                                  db: SessionLocal):

        local_dao = LocalDAO()
        branch_entity_status = local_dao.register_account(manager_entity=manager_entity,
                                                                legal_representative_entity=legal_representative_entity,
                                                                restaurant_entity=restaurant_entity,
                                                                branch_entity=branch_entity,
                                                                branch_bank_entity=branch_bank_entity,
                                                                db=db)

        if type(branch_entity_status) is str:
            return self.parse_error_response_database(message=branch_entity_status)

        return branch_entity_status

    async def delete_credentials(self, uid):
        logger.info('uid: {},', uid)
        firebase_service = FirebaseService()
        await firebase_service.delete_account(uid=uid)
        pass

    def get_account_pre_login(self, email: str, db: SessionLocal):
        logger.info('email: {}', email)
        local_validator = LocalValidator()
        validated_email = local_validator.validate_email(email=email)  # TODO: Refactorizar

        if validated_email:
            logger.error("validated_data: {}", validated_email)
            self.raise_custom_error(message=validated_email)

        local_dao = LocalDAO()
        account_pre_login = local_dao.get_account_pre_login(email=email, db=db)

        if type(account_pre_login) is str or not account_pre_login:
            logger.error("account_pre_login: {}", account_pre_login)
            self.raise_custom_error(message=account_pre_login)

        branch_mapper_request = BranchMapperRequest()
        return branch_mapper_request.to_branch_create_response(body=account_pre_login)

    def get_account_profile(self, email: str, db: SessionLocal):
        logger.info('email: {}', email)
        local_validator = LocalValidator()
        validated_email = local_validator.validate_email(email=email)

        if validated_email: # TODO: Refactorizar
            logger.error("validated_data: {}", validated_email)
            self.raise_custom_error(message=validated_email)

        local_dao = LocalDAO()
        branch_profile = local_dao.get_account_profile(email=email, db=db)

        if type(branch_profile) is str or not branch_profile:
            logger.error("account_pre_login: {}", branch_profile)
            self.raise_custom_error(message=branch_profile)

        branch_mapper_request = BranchMapperRequest()
        return branch_mapper_request.to_branch_create_response(body=branch_profile)

    def raise_custom_error(self, message):
        raise CustomError(name="Error al registrar cuenta de local",
                          detail=message,
                          status_code=status.HTTP_400_BAD_REQUEST if message else status.HTTP_204_NO_CONTENT,
                          cause="")  # TODO: Llenar campo

    def parse_error_response_database(self, message):

        if self.LEGAL_REPRESENTATIVE_KEY_WORD in message:
            return self.LEGAL_REPRESENTATIVE_ERROR_MESSAGE

        if self.RESTAURANT_KEY_WORD in message:
            return self.RESTAURANT_ERROR_MESSAGE

        return self.STANDARD_ERROR_MESSAGE
