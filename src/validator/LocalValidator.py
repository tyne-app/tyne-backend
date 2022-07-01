import re

from fastapi import status
from loguru import logger

from src.dto.request.business_request_dto import NewAccount, Branch, Restaurant, LegalRepresentative, Manager, \
    BranchBank, \
    NewBranch
from src.exception.exceptions import CustomError
from src.util.Constants import Constants
from src.exception.exceptions import CustomError


class LocalValidator:
    NUMBER_AND_WORD_REGEX = re.compile(r"[A-Za-z0-9\sáéíóúÁÉÍÓÚñ]+")
    NUMBER_REGEX = re.compile(r"[0-9]+")
    IDENTIFIER_REGEX = re.compile(r"[0-9]{7,}[0-9K]")
    BASE_COMMERCIAL_IDENTIFIER_NUMBER = 70000000
    BASE_PERSON_IDENTIFIER_NUMBER = 4000000
    PHONE_REGEX = re.compile(r"\+569[0-9]{8}")
    ADDRESS_REGEX = re.compile(r"[^\"\\#$%&()=?¡¿'+´{}\-_:,;|~`^¬\[\]@]+")
    EMAIL_REGEX = re.compile(r"[A-Za-z0-9\.]+@[A-Za-z0-9]+\.?[A-Za-z]+")
    PASSWORD_REGEX = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z\d$@$!%*?&].{7,}")
    VALID_STATE_ID = range(83, 134)
    INVALID_DATA_MESSAGE = "Formato no válido"
    INVALID_DATA_PHONE_MESSAGE = "Formato de teléfono {0} no válido"
    INVALID_DATA_NAME_MESSAGE = "Formato del nombre {0} no válido"
    INVALID_DATA_LAST_NAME_MESSAGE = "Formato del apellido {0} no válido"
    INVALID_DATA_EMAIL_MESSAGE = "Formato de correo {0} no válido"
    INVALID_DATA_PASSWORD_MESSAGE = "Formato de contraseña {0} no válido"
    INVALID_DATA_IDENTIFIER_MESSAGE = "Formato de identificacón {0} no válido"
    INVALID_DATA_COMMERCIAL_ACTIVITY_MESSAGE = "Formato del giro de local no válido"
    INVALID_DATA_STREET_MESSAGE = "Formato de calle {0} no válido"
    INVALID_DATA_NUMBER_STREET_MESSAGE = "Formato de número de calle {0} no válido"
    INVALID_DATA_STATE_ID_MESSAGE = "Formato comuna no válido"
    INVALID_DATA_ACCEPT_PET_MESSAGE = "Formato de aceptación de mascotas no válido"
    INVALID_ACCOUNT_NUMBER = "Formato número de cuenta no válido"
    INVALID_STATE_ID_CITY = "Ciudad no valida"

    LEGAL_REPRESENTATIVE = "del representante legal"
    MANAGER = "del encargado"
    RESTAURANT = "de la casa matriz"
    BRANCH = "del local"

    def validate_new_account(self, new_account: NewAccount):
        data_checked = []
        manager_checked = self.validate_manager(manager=new_account.manager)
        if bool(manager_checked):
            data_checked.append(manager_checked)

        legal_representative_checked = self.validate_legal_representative(
            legal_representative=new_account.legal_representative)
        if bool(legal_representative_checked):
            data_checked.append(legal_representative_checked)

        restaurant_checked = self.validate_restaurant(restaurant=new_account.restaurant)
        if bool(restaurant_checked):
            data_checked.append(restaurant_checked)

        branch_checked = self.validate_branch(branch=new_account.branch)
        if bool(branch_checked):
            data_checked.append(branch_checked)

        branch_bank_checked = self.validate_branch_bank(branch_bank=new_account.branch_bank)
        if bool(branch_bank_checked):
            data_checked.append(branch_bank_checked)

        if data_checked:
            logger.error("data_checked: {}", data_checked)
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=data_checked,
                              status_code=status.HTTP_400_BAD_REQUEST)
        return data_checked

    def validate_manager(self, manager: Manager):
        logger.info('manager: {}', manager)
        invalid_data = []
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, manager.name):
            invalid_data.append(self.INVALID_DATA_NAME_MESSAGE.replace("{0}", self.MANAGER))
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, manager.last_name):
            invalid_data.append(self.INVALID_DATA_LAST_NAME_MESSAGE.replace("{0}", self.MANAGER))
        if not re.fullmatch(self.PHONE_REGEX, manager.phone):
            invalid_data.append((self.INVALID_DATA_PHONE_MESSAGE.replace("{0}", self.MANAGER)))
        if not re.fullmatch(self.EMAIL_REGEX, manager.email):
            invalid_data.append(self.INVALID_DATA_EMAIL_MESSAGE.replace("{0}", self.MANAGER))
        if not re.fullmatch(self.PASSWORD_REGEX, manager.password):
            invalid_data.append(self.INVALID_DATA_PASSWORD_MESSAGE.replace("{0}", self.MANAGER))
        if invalid_data:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)
        return invalid_data

    def validate_legal_representative(self, legal_representative: LegalRepresentative):
        logger.info('legal_representative: {}', legal_representative)

        invalid_data = []
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, legal_representative.name):
            invalid_data.append(self.INVALID_DATA_NAME_MESSAGE.replace("{0}", self.LEGAL_REPRESENTATIVE))
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, legal_representative.last_name):
            invalid_data.append(self.INVALID_DATA_LAST_NAME_MESSAGE.replace("{0}", self.LEGAL_REPRESENTATIVE))
        if not re.fullmatch(self.IDENTIFIER_REGEX, legal_representative.identifier) or \
                int(legal_representative.identifier[:-1]) < self.BASE_PERSON_IDENTIFIER_NUMBER:
            invalid_data.append(self.INVALID_DATA_IDENTIFIER_MESSAGE.replace("{0}", self.LEGAL_REPRESENTATIVE))
        if not re.fullmatch(self.EMAIL_REGEX, legal_representative.email):
            invalid_data.append(self.INVALID_DATA_EMAIL_MESSAGE.replace("{0}", self.LEGAL_REPRESENTATIVE))
        if not re.fullmatch(self.PHONE_REGEX, legal_representative.phone):
            invalid_data.append(self.INVALID_DATA_PHONE_MESSAGE.replace("{0}", self.LEGAL_REPRESENTATIVE))

        if invalid_data:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)

        return invalid_data

    def validate_restaurant(self, restaurant: Restaurant):
        logger.info('restaurant: {}', restaurant)
        invalid_data = []
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, restaurant.name):
            invalid_data.append('Nombre de local inválido')
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, restaurant.commercial_activity):
            invalid_data.append(self.INVALID_DATA_COMMERCIAL_ACTIVITY_MESSAGE)
        if not re.fullmatch(self.IDENTIFIER_REGEX, restaurant.identifier) or \
                int(restaurant.identifier[:-1]) < self.BASE_COMMERCIAL_IDENTIFIER_NUMBER:
            invalid_data.append(self.INVALID_DATA_IDENTIFIER_MESSAGE.replace("{0}", self.RESTAURANT))
        if not re.fullmatch(self.ADDRESS_REGEX, restaurant.street.strip()):
            invalid_data.append(self.INVALID_DATA_STREET_MESSAGE.replace("{0}", self.RESTAURANT))
        if type(restaurant.street_number) != int:
            invalid_data.append(self.INVALID_DATA_NUMBER_STREET_MESSAGE)
        if not re.fullmatch(self.PHONE_REGEX, restaurant.phone):
            invalid_data.append(self.INVALID_DATA_PHONE_MESSAGE.replace("{0}", self.RESTAURANT))
        if type(restaurant.state_id) != int:
            invalid_data.append(self.INVALID_DATA_STATE_ID_MESSAGE)
        if restaurant.state_id not in self.VALID_STATE_ID:
            invalid_data.append(self.INVALID_STATE_ID_CITY)
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, restaurant.name):
            invalid_data.append(self.INVALID_DATA_NAME_MESSAGE.replace("{0}", self.BRANCH))

        if invalid_data:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)

        return invalid_data

    def validate_branch(self, branch: Branch):
        logger.info('branch: {}', branch)

        invalid_data = []
        if not re.fullmatch(self.ADDRESS_REGEX, branch.street.strip()):
            print(branch.street)
            invalid_data.append(self.INVALID_DATA_STREET_MESSAGE.replace("{0}", self.BRANCH))
        if type(branch.street_number) != int:
            invalid_data.append(self.INVALID_DATA_NUMBER_STREET_MESSAGE.replace("{0}", self.BRANCH))
        if type(branch.state_id) != int:
            invalid_data.append(self.INVALID_DATA_STATE_ID_MESSAGE)
        if type(branch.accept_pet) != bool:
            invalid_data.append(self.INVALID_DATA_ACCEPT_PET_MESSAGE)

        if invalid_data:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)
        return invalid_data

    def validate_branch_bank(self, branch_bank: BranchBank):
        logger.info('branch_bank: {}', branch_bank)

        invalid_data = []
        if not re.fullmatch(self.NUMBER_REGEX, branch_bank.account_holder_identifier):
            invalid_data.append(self.INVALID_DATA_MESSAGE)
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, branch_bank.account_holder_name):
            invalid_data.append(self.INVALID_DATA_MESSAGE)
        if not re.fullmatch(self.NUMBER_REGEX, branch_bank.account_number):
            invalid_data.append(self.INVALID_ACCOUNT_NUMBER)
        if type(branch_bank.bank_id) != int:
            invalid_data.append(self.INVALID_DATA_MESSAGE)
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, branch_bank.account_type):
            invalid_data.append(self.INVALID_DATA_MESSAGE)

        if invalid_data:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)
        return invalid_data

    def validate_second_branch(self, new_branch: NewBranch):
        logger.info('new_branch: {}', NewBranch)

        invalid_data = []
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, new_branch.branch.street):
            invalid_data.append(self.INVALID_DATA_MESSAGE)
        if type(new_branch.branch.street_number) != int:
            invalid_data.append(self.INVALID_DATA_MESSAGE)
        if type(new_branch.branch.state_id) != int:
            invalid_data.append(self.INVALID_DATA_MESSAGE)
        if type(new_branch.branch.accept_pet) != bool:
            invalid_data.append(self.INVALID_DATA_MESSAGE)

        if invalid_data:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)
        return invalid_data

    def validate_new_branch(self, new_branch: NewBranch):
        logger.info('new_branch: {}', new_branch)
        data_checked = []

        manager_checked = self.validate_manager(manager=new_branch.manager)
        if bool(manager_checked):
            data_checked.append(manager_checked)

        branch_checked = self.validate_second_branch(new_branch=new_branch)
        if bool(branch_checked):
            data_checked.append(branch_checked)
        branch_bank_checked = self.validate_branch_bank(branch_bank=new_branch.branch_bank)

        if bool(branch_bank_checked):
            data_checked.append(branch_bank_checked)

        if data_checked:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=data_checked,
                              status_code=status.HTTP_400_BAD_REQUEST)
        return data_checked

    async def raise_custom_error(self, message):
        raise CustomError(name=Constants.INVALID_DATA_ERROR,
                          detail=message,
                          status_code=status.HTTP_400_BAD_REQUEST)
