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

    async def create_new_account(self, new_account: NewAccount, db: SessionLocal):
        logger.info('new_account: {}', new_account)

        local_validator = LocalValidator()
        validated_data = local_validator.validate_new_account(new_account=new_account)

        if validated_data:
            logger.error("validated_data: {}", validated_data)
            raise CustomError(name="Error validación de datos",
                              detail=validated_data,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="")  # TODO: Llenar campo

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
            raise CustomError(name="Error al registrar cuenta de local",
                              detail=branch_entity_status,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="")  # TODO: Llenar campo

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

        # TODO: Definir: Si respuesta a registrar cuenta es String, llamar función para convertir respuesta a español.
        return branch_entity_status

    async def delete_credentials(self, uid):
        firebase_service = FirebaseService()
        await firebase_service.delete_account(uid=uid)
        pass
