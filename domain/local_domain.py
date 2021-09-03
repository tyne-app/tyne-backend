from loguru import logger
from validator.local_validator import validate_new_account
from schema.local_schemas import CreateAccount, CreateAccountMSLocal, Manager
from integration.integrations import FirebaseIntegrationApiClient, MSLocalClient, MapBoxIntegrationClient
from dto.dto import GenericDTO as LocalDTO

MANAGER_INDEX = 0
OWNER_INDEX = 1
MSG_ERROR_FIREBASE = "No se puede crear credenciales, usuario existente"
MSG_ERROR_MS_LOCAL = "Error al registrar datos de sucursal"
MSG_ERROR_BRANCH_ADDRESS = "Dirección de local no válida"
LEGAL_REPRESENTATIVE_MSG_ERROR = "Rut representante legal ya registrado"
LEGAL_REPRESENTATIVE_KEY = "legal_representative"
RESTAURANT_MSG_ERROR = "Rut restaurant ya registrado"
RESTAURANT_KEY = "restaurant"

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

    uid = await create_account_firebase(new_account=new_account, firebase_api_client=firebase_api_client)

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


async def create_account_firebase(new_account: CreateAccount, firebase_api_client: FirebaseIntegrationApiClient):

    credentials = get_credentials(Manager(**new_account.legal_representative[0].dict()))
    uid = await firebase_api_client.create_account(email=credentials["email"], password=credentials["password"])
    return uid


def get_credentials(manager: Manager) -> dict:
    credentials = {
        "email": manager.email,
        "password": manager.password
    }
    return credentials


async def create_account_db(new_account: CreateAccount, uid: str, firebase_api_client: FirebaseIntegrationApiClient):
    ms_local = MSLocalClient()
    new_account_dict = await define_create_account_data(new_account=new_account, uid=uid)

    if type(new_account_dict) == str:
        logger.info("new_account_dict: {}", new_account_dict)
        await firebase_api_client.delete_account(uid)
        return new_account_dict

    logger.info("new_account_dict: {}", new_account_dict)

    new_account_response = await ms_local.create_account(new_account=new_account_dict)
    logger.info("new_account_id: {}", new_account_response)

    if type(new_account_response) == str and type(uid) == str:
        await firebase_api_client.delete_account(uid)
        return LEGAL_REPRESENTATIVE_MSG_ERROR \
            if LEGAL_REPRESENTATIVE_KEY in new_account_response \
            else RESTAURANT_MSG_ERROR

    return new_account_response


async def define_create_account_data(new_account: CreateAccount, uid: str):
    mapbox_client = MapBoxIntegrationClient()

    manager = new_account.legal_representative[MANAGER_INDEX].dict()
    logger.info("manager: {}", manager)
    del(manager["password"])

    owner = new_account.legal_representative[OWNER_INDEX].dict()
    logger.info("owner: {}", owner)

    branch = dict(new_account.branch)
    branch["uid"] = uid

    coordinates = await mapbox_client.get_latitude_longitude(address=f"{branch['address']} Chile")
    logger.info("coordinates: {}", coordinates)

    if not coordinates:
        return MSG_ERROR_BRANCH_ADDRESS

    branch["latitude"] = coordinates["latitude"]
    branch["longitude"] = coordinates["longitude"]

    new_account_dict = {
        "legal_representative": [manager, owner],
        "branch": branch,
        "restaurant": new_account.restaurant.dict(),
        "bank_restaurant": new_account.bank_restaurant.dict()
    }
    logger.info("new_account_dict: {}", new_account_dict)
    return new_account_dict


def define_response(data):  # TODO:  Crear funcion para crear respuesta estandar
    logger.info("data: {}", data)
    pass


