import re
from loguru import logger
from dto.request.local_request_dto import NewAccount, Branch, Restaurant, LegalRepresentative, Manager, BranchBank,\
    NewBranch


class LocalValidator:

    NUMBER_AND_WORD_REGEX = re.compile(r"[A-Za-z0-9\sáéíóúÁÉÍÓÚñ]+")
    NUMBER_REGEX = re.compile(r"[0-9]+")
    PHONE_REGEX = re.compile(r"\+569[0-9]{8}")
    ADDRESS_REGEX = re.compile(r"[A-Za-z\s\.0-9#áéíóúÁÉÍÓÚ]+")
    EMAIL_REGEX = re.compile(r"[A-Za-z0-9\.]+@[A-Za-z0-9]+\.?[A-Za-z]+")
    INVALID_DATA_MESSAGE = "Formato no válido"

    def validate_email(self, email: str):
        logger.info("email: {}", email)

        data_checked = {}

        if not re.fullmatch(self.EMAIL_REGEX, email):
            data_checked["email"] = self.INVALID_DATA_MESSAGE

        return data_checked

    def validate_new_account(self, new_account: NewAccount):
        data_checked = {}

        manager_checked = self.validate_manager(manager=new_account.manager)
        if bool(manager_checked):
            data_checked["manager"] = manager_checked

        legal_representative_checked = self.validate_legal_representative(legal_representative=new_account.legal_representative)
        if bool(legal_representative_checked):
            data_checked["legal_representative"] = legal_representative_checked

        restaurant_checked = self.validate_restaurant(restaurant=new_account.restaurant)
        if bool(restaurant_checked):
            data_checked["restaurant"] = restaurant_checked

        branch_checked = self.validate_branch(branch=new_account.branch)
        if bool(branch_checked):
            data_checked["branch"] = branch_checked

        branch_bank_checked = self.validate_branch_bank(branch_bank=new_account.branch_bank)
        if bool(branch_bank_checked):
            data_checked["branch_bank_checked"] = branch_bank_checked

        return data_checked

    def validate_manager(self, manager: Manager):
        logger.info('manager: {}', manager)

        invalid_data = {}
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, manager.name):
            invalid_data["name"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, manager.last_name):
            invalid_data["last_name"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.PHONE_REGEX, manager.phone):
            invalid_data["phone"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.EMAIL_REGEX, manager.email):
            invalid_data["email"] = self.INVALID_DATA_MESSAGE
        # TODO: Incluir contraseña cuando se tenga las reglas de seguridad
        return invalid_data

    def validate_legal_representative(self, legal_representative: LegalRepresentative):
        logger.info('legal_representative: {}', legal_representative)

        invalid_data = {}
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, legal_representative.name):
            invalid_data["name"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, legal_representative.last_name):
            invalid_data["last_name"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_REGEX, legal_representative.identifier):
            invalid_data["identifier"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.EMAIL_REGEX, legal_representative.email):
            invalid_data["email"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.PHONE_REGEX, legal_representative.phone):
            invalid_data["phone"] = self.INVALID_DATA_MESSAGE

        return invalid_data

    def validate_restaurant(self, restaurant: Restaurant):
        logger.info('restaurant: {}', restaurant)

        invalid_data = {}
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, restaurant.social_reason):
            invalid_data["social_reason"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, restaurant.commercial_activity):
            invalid_data["commercial_activity"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_REGEX, restaurant.identifier):
            invalid_data["identifier"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.ADDRESS_REGEX, restaurant.street):
            invalid_data["street"] = self.INVALID_DATA_MESSAGE
        if type(restaurant.street_number) != int:
            invalid_data["street_number"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.PHONE_REGEX, restaurant.phone):
            invalid_data["phone"] = self.INVALID_DATA_MESSAGE
        if type(restaurant.state_id) != int:
            invalid_data["state_id"] = self.INVALID_DATA_MESSAGE

        return invalid_data

    def validate_branch(self, branch: Branch):
        logger.info('branch: {}', branch)

        invalid_data = {}
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, branch.name):
            invalid_data["name"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.ADDRESS_REGEX, branch.street):
            invalid_data["street"] = self.INVALID_DATA_MESSAGE
        if type(branch.street_number) != int:
            invalid_data["street_number"] = self.INVALID_DATA_MESSAGE
        if type(branch.state_id) != int:
            invalid_data["state_id"] = self.INVALID_DATA_MESSAGE
        if type(branch.accept_pet) != bool:
            invalid_data["accept_pet"] = self.INVALID_DATA_MESSAGE

        return invalid_data

    def validate_branch_bank(self, branch_bank: BranchBank):
        logger.info('branch_bank: {}', branch_bank)

        invalid_data = {}
        if not re.fullmatch(self.NUMBER_REGEX, branch_bank.account_holder_identifier):
            invalid_data["account_holder_identifier"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, branch_bank.account_holder_name):
            invalid_data["account_holder_name"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_REGEX, branch_bank.account_number):
            invalid_data["account_number"] = self.INVALID_DATA_MESSAGE
        if type(branch_bank.bank_id) != int:
            invalid_data["bank_id"] = self.INVALID_DATA_MESSAGE
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, branch_bank.account_type):
            invalid_data["account_type"] = self.INVALID_DATA_MESSAGE
        return invalid_data

    def validate_second_branch(self, new_branch: NewBranch):
        logger.info('new_branch: {}', NewBranch)

        invalid_data = {}
        if not re.fullmatch(self.NUMBER_AND_WORD_REGEX, new_branch.street):
            invalid_data["street"] = self.INVALID_DATA_MESSAGE
        if type(new_branch.street_number) != int:
            invalid_data["street_number"] = self.INVALID_DATA_MESSAGE
        if type(new_branch.state_id) != int:
            invalid_data["state_id"] = self.INVALID_DATA_MESSAGE
        if type(new_branch.accept_pet) != bool:
            invalid_data["accept_pet"] = self.INVALID_DATA_MESSAGE
        return invalid_data

    def validate_new_branch(self, new_branch: NewBranch):
        logger.info('new_branch: {}', new_branch)

        data_checked = {}

        manager_checked = self.validate_manager(manager=new_branch.manager)
        if bool(manager_checked):
            data_checked["manager"] = manager_checked
        branch_checked = self.validate_second_branch(new_branch=new_branch.new_branch)
        if bool(branch_checked):
            data_checked["new_branch"] = branch_checked
        branch_bank_checked = self.validate_branch_bank(branch_bank=new_branch.branch_bank)
        if bool(branch_bank_checked):
            data_checked["branch_bank"] = branch_bank_checked

        return data_checked
