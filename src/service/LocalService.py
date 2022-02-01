from loguru import logger
from sqlalchemy.orm import Session

from src.dto.request.business_request_dto import NewAccount
from src.dto.request.business_request_dto import NewBranch
from src.mappers.request.BusinessMapperRequest import BusinessMapperRequest
from src.repository.dao.LocalDao import LocalDAO
from src.repository.dao.StateDao import StateDao
from src.service.MapboxService import MapBoxService
from src.util.EmailSubject import EmailSubject
from src.validator.LocalValidator import LocalValidator
from src.service.EmailService import EmailService
from src.util.Constants import Constants

class LocalService:
    MSG_CREATE_ACCOUNT_SUCCESSFULLY = "Local creado correctamente"
    MSG_ERROR_BRANCH_ADDRESS = "Dirección de local no válida"
    LEGAL_REPRESENTATIVE_IDENTIFIER_KEY_WORD = 'legal_representative_identifier_key'
    LEGAL_REPRESENTATIVE_IDENTIFIER_ERROR_MESSAGE = 'Rut representante legal ya está registrado'
    LEGAL_REPRESENTATIVE_EMAIL_KEY_WORD = 'legal_representative_email_key'
    LEGAL_REPRESENTATIVE_EMAIL_ERROR_MESSAGE = 'Email representante legal ya está registrado'
    RESTAURANT_KEY_WORD = 'restaurant_identifier_key'
    RESTAURANT_ERROR_MESSAGE = 'Rut restaurant ya está registrado'
    STANDARD_ERROR_MESSAGE = 'Error en base de datos'
    CREATE_ACCOUNT_ERROR_MSG = 'Error al registrar cuenta de local'
    GET_PROFILE_ERROR_MSG = 'Error al obtener perfil sucursal'
    NEW_BRANCH_ERROR_MSG = 'Error al agregar una sucursal nueva'
    MANAGER_EMAIL_KEY_WORD = 'user_un_email'
    MANAGER_EMAIL_ERROR_MESSAGE = 'Email manager ya está registrado'
    MSG_NEW_BRANCH = 'Sucursal agregado correctamente'
    ID_USER_TYPE = 1
    _business_mapper_request = BusinessMapperRequest()
    DEFAULT_LOCAL_IMAGE_PROFILE = "https://res.cloudinary.com/dqdtvbynk/image/upload/v1636295279/Development/users/default%20main%20local%20image/Sart%C3%A9n_Tyne_Fondo_Transparente_zflbrr.png"
    _email_service = EmailService()
    _local_dao = LocalDAO()
    _state_dao_ = StateDao()

    async def create_new_account(self, new_account: NewAccount, db: Session):
        local_validator = LocalValidator()
        local_validator.validate_new_account(new_account=new_account)
        print(new_account.restaurant.description) # TODO: Reemplazar por log
        branch = new_account.branch

        state = self._state_dao_.get_state_by_id(id_state=branch.state_id, db=db)

        branch_geocoding = await self.geocoding(street=branch.street, street_number=branch.street_number,
                                                state_name=state.name)

        manager = new_account.manager

        user = {'email': manager.email, 'password': manager.password}
        user_entity = self._business_mapper_request.to_user_entity(user_dict=user, id_user_type=self.ID_USER_TYPE)

        manager_entity = self._business_mapper_request.to_manager_entity(manager=manager)

        legal_representative = new_account.legal_representative
        legal_representative_entity = self._business_mapper_request. \
            to_legal_representative_entity(legal_representative=legal_representative)

        restaurant = new_account.restaurant
        restaurant_entity = self._business_mapper_request.to_restaurant_entity(restaurant=restaurant, name=branch.name)

        branch_entity = self._business_mapper_request.to_branch_entity(branch=branch, branch_geocoding=branch_geocoding)

        branch_bank = new_account.branch_bank
        branch_bank_entity = self._business_mapper_request.to_branch_bank_entity(branch_bank=branch_bank)

        branch_image_entity = self._business_mapper_request. \
            to_branch_image_entity(default_main_image=self.DEFAULT_LOCAL_IMAGE_PROFILE)

        local_dao = LocalDAO()
        local_dao.register_account(user_entity=user_entity,
                                   manager_entity=manager_entity,
                                   legal_representative_entity=legal_representative_entity,
                                   restaurant_entity=restaurant_entity,
                                   branch_entity=branch_entity,
                                   branch_bank_entity=branch_bank_entity,
                                   branch_image_entity=branch_image_entity,
                                   db=db)

        self._email_service.send_email(user=Constants.LOCAL, subject=EmailSubject.WELCOME, receiver_email=manager.email)

        return self._business_mapper_request.to_branch_create_response(content=self.MSG_CREATE_ACCOUNT_SUCCESSFULLY)

    async def geocoding(self, street: str, street_number: int, state_name: str):
        mapbox_service = MapBoxService()
        address = street + " " + str(street_number)
        coordinates = await mapbox_service.get_latitude_longitude(address=address, state_name=state_name)
        return coordinates

    def get_account_profile(self, branch_id: int, db: Session):
        return self._local_dao.get_account_profile(branch_id=branch_id, db=db)

    async def add_new_branch(self, branch_id, new_branch: NewBranch, db: Session):
        local_validator = LocalValidator()
        local_validator.validate_new_branch(new_branch=new_branch)

        branch = new_branch.branch

        state = self._state_dao_.get_state_by_id(id_state=branch.state_id, db=db)

        branch_geocoding = await self.geocoding(street=branch.street, street_number=branch.street_number,
                                                state_name=state.name)
        manager = new_branch.manager

        user = {'email': manager.email, 'password': manager.password}
        user_entity = self._business_mapper_request.to_user_entity(user_dict=user, id_user_type=self.ID_USER_TYPE)

        manager_entity = self._business_mapper_request.to_manager_entity(manager=manager)

        branch_entity = self._business_mapper_request.to_branch_entity(branch=branch,
                                                                       branch_geocoding=branch_geocoding)
        branch_bank = new_branch.branch_bank
        branch_bank_entity = self._business_mapper_request.to_branch_bank_entity(branch_bank=branch_bank)

        branch_image_entity = self._business_mapper_request \
            .to_branch_image_entity(default_main_image=self.DEFAULT_LOCAL_IMAGE_PROFILE)

        new_branch_status = self._local_dao.add_new_branch(user_entity=user_entity,
                                                           branch_id=branch_id,
                                                           manager_entity=manager_entity,
                                                           branch_entity=branch_entity,
                                                           branch_bank_entity=branch_bank_entity,
                                                           branch_image_entity=branch_image_entity,
                                                           db=db)

        logger.info('new_branch_status: {}', new_branch_status)

        return True
