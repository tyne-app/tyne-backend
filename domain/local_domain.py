from loguru import logger

from dto.dto import GenericDTO as LocalDTO
from integration.integrations import FirebaseIntegrationApiClient, MSLocalClient, MapBoxIntegrationClient, MSIntegrationApi
from schema.local_schemas import CreateAccount, Manager, AddBranch
from validator.local_validator import validate_new_account, validate_email, validate_new_branch

MANAGER_INDEX = 0
OWNER_INDEX = 1

MANAGER_ID = 2
OWNER_ID = 1

MSG_ERROR_FIREBASE = "No se puede crear credenciales, usuario existente"
MSG_ERROR_MS_LOCAL = "Error al registrar datos de sucursal"
MSG_ERROR_BRANCH_ADDRESS = "Dirección de local no válida"
LEGAL_REPRESENTATIVE_MSG_ERROR = "Rut representante legal ya registrado"
LEGAL_REPRESENTATIVE_KEY = "legal_representative"
RESTAURANT_MSG_ERROR = "Rut restaurant ya registrado"
RESTAURANT_KEY = "restaurant"
BASE_COUNTRY = "Chile"

async def create_account(new_account: CreateAccount):
    logger.info("new_account: {}", new_account)
    local_dto = LocalDTO()

    validated_data = validate_new_account(new_account=new_account)

    if validated_data:
        logger.error("validated_data: {}", validated_data)
        local_dto.error = validated_data
        return local_dto.__dict__

    logger.info("validated_data: {}", validated_data)

    firebase_api_client = FirebaseIntegrationApiClient()

    uid = await create_account_firebase(new_account=new_account.legal_representative[0])

    if not uid:
        logger.error("uid: {}", uid)
        local_dto.error = MSG_ERROR_FIREBASE
        return local_dto.__dict__

    logger.info("uid: {}", uid)

    new_account_response = await create_account_db(new_account=new_account, uid=uid, firebase_api_client=firebase_api_client)

    if type(new_account_response) == str:
        logger.error("new_account_id: {}", new_account_response)
        local_dto.error = new_account_response
        return local_dto.__dict__

    logger.info("new_account_response: {}", new_account_response)
    local_dto.data = new_account_response
    return local_dto.__dict__


async def create_account_firebase(manager: Manager):

    firebase_api_client = FirebaseIntegrationApiClient()
    credentials = get_credentials(manager=manager)
    uid = await firebase_api_client.create_account(email=credentials["email"], password=credentials["password"])
    return uid


def get_credentials(manager: Manager) -> dict:
    credentials = {
        "email": manager.email,
        "password": manager.password
    }
    return credentials


async def geocoding(street: str, street_number: int):
    logger.info('street: {}, street_number: {}', street, street_number)
    mapbox_client = MapBoxIntegrationClient()

    address = street + " " + str(street_number) + " " + BASE_COUNTRY
    logger.info('address: {}', address)

    coordinates = await mapbox_client.get_latitude_longitude(address=address)
    logger.info("coordinates: {}", coordinates)

    if not coordinates:
        logger.error('geocoding_data: {}', coordinates)
        return MSG_ERROR_BRANCH_ADDRESS

    return coordinates


async def delete_firebase_credentials(uid: str):
    firebase_api_client = FirebaseIntegrationApiClient()
    response = await firebase_api_client.delete_account(uid)

    if type(response) != bool:
        logger.error('response: {}', response)
        return response
    logger.info('response: {}', response)
    return response  # TODO: Ver cómo manejar error al eliminar credenciales.


async def create_account_db(new_account: CreateAccount, uid: str):
    ms_local = MSLocalClient()
    new_account_dict = await define_create_account_data(new_account=new_account, uid=uid)  # TODO: Esto debe estar en funcion principal para evitar recursivdad

    if type(new_account_dict) == str:
        logger.info("new_account_dict: {}", new_account_dict)
        await delete_firebase_credentials(uid=uid)
        return new_account_dict

    logger.info("new_account_dict: {}", new_account_dict)

    new_account_response = await ms_local.create_account(new_account=new_account_dict)
    logger.info("new_account_id: {}", new_account_response)

    if type(new_account_response) == str and type(uid) == str:
        await delete_firebase_credentials(uid=uid)
        return LEGAL_REPRESENTATIVE_MSG_ERROR \
            if LEGAL_REPRESENTATIVE_KEY in new_account_response \
            else RESTAURANT_MSG_ERROR

    return new_account_response


async def define_create_account_data(new_account: CreateAccount, uid: str):
    manager = new_account.legal_representative[MANAGER_INDEX].dict()
    logger.info("manager: {}", manager)
    del(manager["password"])

    owner = new_account.legal_representative[OWNER_INDEX].dict()
    logger.info("owner: {}", owner)

    branch = dict(new_account.branch)
    branch["uid"] = uid

    coordinates = await geocoding(street=branch["street"], street_number=branch["street_number"])  # TODO: Puede que de error esto
    logger.info("coordinates: {}", coordinates)

    if type(coordinates) != dict:
        return MSG_ERROR_BRANCH_ADDRESS

    branch["latitude"] = coordinates["latitude"]
    branch["longitude"] = coordinates["longitude"]

    restaurant = new_account.restaurant.dict()
    restaurant["name"] = branch["name"]

    del(branch["name"])

    new_account_dict = {
        "legal_representative": [manager, owner],
        "branch": branch,
        "restaurant": restaurant,
        "bank_restaurant": new_account.bank_restaurant.dict()
    }
    logger.info("new_account_dict: {}", new_account_dict)
    return new_account_dict


async def get_branch_pre_login(email: str):
    ms_local_client = MSLocalClient()
    local_dto = LocalDTO()

    validated_data = validate_email(email=email)

    if validated_data:
        logger.error("validated_data: {}", validated_data)
        local_dto.error = validated_data
        return local_dto.__dict__

    branch_pre_login = await ms_local_client.get_account_pre_login(email=email)

    if type(branch_pre_login) == str:
        local_dto.error = branch_pre_login
        return local_dto.__dict__

    local_dto.data = branch_pre_login
    return local_dto.__dict__


async def get_branch_profile(email: str):
    ms_local_client = MSLocalClient()
    local_dto = LocalDTO()

    validated_data = validate_email(email=email)

    if validated_data:
        logger.error("validated_data: {}", validated_data)
        local_dto.error = validated_data
        return local_dto.__dict__

    branch_profile = await ms_local_client.get_account(email=email)
    if type(branch_profile) == str:
        local_dto.error = branch_profile
        return local_dto.__dict__

    local_dto.data = branch_profile
    return local_dto.__dict__


async def add_new_branch(new_branch: AddBranch, client_token: str):
    logger.info("new_branch: {}", new_branch)
    local_dto = LocalDTO()

    validated_data = validate_new_branch(new_branch=new_branch)

    if validated_data:
        logger.error("validated_data: {}", validated_data)
        local_dto.error = validated_data
        return local_dto.__dict__

    # TODO: Obtener branch id de token
    ms_integration_api = MSIntegrationApi()
    branch_id = await ms_integration_api.token_data(client_token=client_token)

    if type(branch_id) != int:
        logger.error("validated_data: {}", validated_data)
        local_dto.error = branch_id
        return local_dto.__dict__

    # TODO: Validar transformación street + street_number a latitude y longitude
    coordinates = await geocoding(street=new_branch.new_branch.street,
                                  street_number=new_branch.new_branch.street_number)

    if type(coordinates) != dict:
        logger.error('coordinates: {}', coordinates)
        local_dto.error = MSG_ERROR_BRANCH_ADDRESS
        return local_dto.__dict__

    # TODO: Crear cuenta en firebase
    uid = await create_account_firebase(manager=new_branch.legal_representative)

    if not uid:
        logger.error("uid: {}", uid)
        local_dto.error = MSG_ERROR_FIREBASE
        return local_dto.__dict__

    logger.info("uid: {}", uid)

    # TODO: Crear JSON para crear cuenta en db

    legal_representative_dict = new_branch.legal_representative.dict()
    del(legal_representative_dict["password"])
    legal_representative_dict["type_legal_representative_id"] = MANAGER_ID
    logger.info('legal_representative_dict: {}', legal_representative_dict)

    branch_dict = new_branch.new_branch.dict()
    branch_dict["uid"] = uid
    branch_dict["latitude"] = coordinates["latitude"]
    branch_dict["longitude"] = coordinates["longitude"]
    logger.info('branch_dict: {}', branch_dict)

    new_branch_dict = {
         'branch_id': branch_id,
         'legal_representative': legal_representative_dict,
         'new_branch': branch_dict,
         'bank_restaurant': new_branch.bank_restaurant.dict()
    }
    logger.info('new_brach_dict: {}', new_branch_dict)

    ms_local_client = MSLocalClient()
    new_branch_id = await ms_local_client.add_branch(new_branch=new_branch_dict)

    # TODO: Si da error, eliminar credenciales de firebas y retornar error
    if type(new_branch_id) == str and type(uid) == str:
        await delete_firebase_credentials(uid=uid)
        local_dto.error = new_branch_id
        return local_dto.__dict__

    logger.info('new_branch_id: {}', new_branch_id)
    local_dto.data = new_branch_id
    logger.info('local_dto: {}', local_dto.__dict__)
    return local_dto.__dict__


def define_response(data):  # TODO:  Crear funcion para crear respuesta estandar
    logger.info("data: {}", data)
    pass


