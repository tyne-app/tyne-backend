import re
from schema.local_schemas import CreateAccount, LegalRepresentative, Branch, Restaurant, BankRestaurant

STRING_REGEX = re.compile(r"[A-Za-z\sáéíóúÁÉÍÓÚ]+")  # TODO: Se podría cambia a nombre más declarativo
NUMBER_REGEX = re.compile(r"[0-9]+")
PHONE_REGEX = re.compile(r"\+569[0-9]{8}")
ADDRESS_REGEX = re.compile(r"[A-Za-z\s\.0-9#áéíóúÁÉÍÓÚ]+")
EMAIL_REGEX = re.compile(r"[A-Za-z0-9\.]+@[A-Za-z0-9]+\.?[A-Za-z]+")
# TODO: Se debe crear respuesta que almacenee indique los campos con valores erróneos

INVALID_DATA_MESSAGE = "Formato no válido"


def validate_new_account(new_account: CreateAccount):
    data_checked = {}

    legal_representative_checked = validate_legal_representative(new_account.legal_representative)
    if bool(legal_representative_checked):
        data_checked["legal_representative"] = legal_representative_checked

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


def validate_legal_representative(legal_representative: LegalRepresentative):

    invalid_data = {}
    if not re.fullmatch(STRING_REGEX,legal_representative.name):
        invalid_data["name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, legal_representative.last_name):
        invalid_data["last_name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(NUMBER_REGEX, legal_representative.identifier):
        invalid_data["identifier"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(EMAIL_REGEX, legal_representative.email):
        invalid_data["email"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(PHONE_REGEX, legal_representative.phone):
        invalid_data["phone"] = INVALID_DATA_MESSAGE

    return invalid_data


def validate_branch(branch: Branch):

    invalid_data = {}
    if not re.fullmatch(STRING_REGEX, branch.name):
        invalid_data["name"] = INVALID_DATA_MESSAGE
    if type(branch.accept_pet) != bool:
        invalid_data["accept_pet"] = INVALID_DATA_MESSAGE

    if not re.fullmatch(STRING_REGEX, branch.commercial_activity):
        invalid_data["commercial_activity"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(ADDRESS_REGEX, branch.address):
        invalid_data["address"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, branch.state):
        invalid_data["state"] = INVALID_DATA_MESSAGE

    return invalid_data


def validate_restaurant(restaurant: Restaurant):

    invalid_data = {}
    if not re.fullmatch(NUMBER_REGEX, restaurant.identifier):
        invalid_data["identifier"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, restaurant.name):
        invalid_data["name"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(ADDRESS_REGEX, restaurant.address):
        invalid_data["address"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, restaurant.state):
        invalid_data["state"] = INVALID_DATA_MESSAGE

    return invalid_data


def validate_bank_restaurant(bank_restaurant: BankRestaurant):

    invalid_data = {}
    if not re.fullmatch(NUMBER_REGEX, bank_restaurant.account_holder_identifier):
        invalid_data["account_holder_identifier"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, bank_restaurant.account_holder):
        invalid_data["account_holder"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(NUMBER_REGEX, bank_restaurant.account_number):
        invalid_data["account_number"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, bank_restaurant.account_type):
        invalid_data["account_type"] = INVALID_DATA_MESSAGE
    if not re.fullmatch(STRING_REGEX, bank_restaurant.bank):
        invalid_data["bank"] = INVALID_DATA_MESSAGE

    return invalid_data

