import re

from loguru import logger

from schema.local_schemas import CreateAccount, Branch, Restaurant, BankRestaurant, Owner, Manager

STRING_REGEX = re.compile(r"[A-Za-z0-9\sáéíóúÁÉÍÓÚñ]+")  # TODO: Se podría cambia a nombre más declarativo
NUMBER_REGEX = re.compile(r"[0-9]+")
PHONE_REGEX = re.compile(r"\+569[0-9]{8}")
ADDRESS_REGEX = re.compile(r"[A-Za-z\s\.0-9#áéíóúÁÉÍÓÚ]+")
EMAIL_REGEX = re.compile(r"[A-Za-z0-9\.]+@[A-Za-z0-9]+\.?[A-Za-z]+")

INVALID_DATA_MESSAGE = "Formato no válido"


def validate_email(email: str):
    data_checked = {}

    if not re.fullmatch(EMAIL_REGEX, email):
        data_checked["email"] = INVALID_DATA_MESSAGE

    return data_checked


def validate_new_account(new_account: CreateAccount):
    data_checked = {}

    manager_checked = validate_manager(Manager(**new_account.legal_representative[0].dict()))
    if bool(manager_checked):
        data_checked["manager"] = manager_checked

    owner_checked = validate_owner(Owner(**new_account.legal_representative[1].dict()))
    if bool(owner_checked):
        data_checked["owner"] = owner_checked

    branch_checked = validate_branch(new_account.branch)
    if bool(branch_checked):
        data_checked["branch"] = branch_checked

    restaurant_checked = validate_restaurant(new_account.restaurant)
    if bool(restaurant_checked):
        data_checked["restaurant"] = restaurant_checked

    bank_restaurant_checked = validate_bank_restaurant(new_account.bank_restaurant)
    if bool(bank_restaurant_checked):
        data_checked["bank_restaurant"] = bank_restaurant_checked

    return data_checked


def validate_manager(manager: Manager):
    logger.info('manager: {}', manager)

    invalid_data = {}
    if not re.fullmatch(STRING_REGEX, manager.name):
        invalid_data["name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, manager.last_name):
        invalid_data["last_name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(PHONE_REGEX, manager.phone):
        invalid_data["phone"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(EMAIL_REGEX, manager.email):
        invalid_data["email"] = INVALID_DATA_MESSAGE
    if manager.type_legal_representative_id != 2:
        invalid_data["type_legal_representative_id"] = INVALID_DATA_MESSAGE

    return invalid_data


def validate_owner(owner: Owner):
    logger.info('owner: {}', owner)

    invalid_data = {}
    if not re.fullmatch(STRING_REGEX, owner.name):
        invalid_data["name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, owner.last_name):
        invalid_data["last_name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(NUMBER_REGEX, owner.identifier):
        invalid_data["identifier"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(PHONE_REGEX, owner.phone):
        invalid_data["phone"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(EMAIL_REGEX, owner.email):
        invalid_data["email"] = INVALID_DATA_MESSAGE
    if owner.type_legal_representative_id != 1:
        invalid_data["type_legal_representative_id"] = INVALID_DATA_MESSAGE

    return invalid_data


def validate_branch(branch: Branch):
    logger.info('branch: {}', branch)

    invalid_data = {}
    if not re.fullmatch(STRING_REGEX, branch.name):
        invalid_data["name"] = INVALID_DATA_MESSAGE
    if type(branch.accept_pet) != bool:
        invalid_data["accept_pet"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, branch.commercial_activity):
        invalid_data["commercial_activity"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(ADDRESS_REGEX, branch.address):
        invalid_data["address"] = INVALID_DATA_MESSAGE
    if type(branch.state_id) != int:
        invalid_data["state_id"] = INVALID_DATA_MESSAGE

    return invalid_data


def validate_restaurant(restaurant: Restaurant):
    logger.info('restaurant: {}', restaurant)

    invalid_data = {}
    if not re.fullmatch(NUMBER_REGEX, restaurant.identifier):
        invalid_data["identifier"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, restaurant.name):
        invalid_data["name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(ADDRESS_REGEX, restaurant.address):
        invalid_data["address"] = INVALID_DATA_MESSAGE
    if type(restaurant.state_id) != int:
        invalid_data["state_id"] = INVALID_DATA_MESSAGE

    return invalid_data


def validate_bank_restaurant(bank_restaurant: BankRestaurant):
    logger.info('bank_restaurant: {}', bank_restaurant)

    invalid_data = {}
    if not re.fullmatch(NUMBER_REGEX, bank_restaurant.account_holder_identifier):
        invalid_data["account_holder_identifier"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, bank_restaurant.account_holder):
        invalid_data["account_holder"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(NUMBER_REGEX, bank_restaurant.account_number):
        invalid_data["account_number"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, bank_restaurant.account_type):
        invalid_data["account_type"] = INVALID_DATA_MESSAGE
    if type(bank_restaurant.bank_id) != int:
        invalid_data["bank_id"] = INVALID_DATA_MESSAGE
    return invalid_data

