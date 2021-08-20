import json
from loguru import logger
from validator.local_validator import validate_new_account
from schema.local_schemas import CreateAccount, CreateAccountMSLocal
from integration.integrations import FirebaseIntegrationApiClient, MSLocalClient
from dto.dto import GenericDTO as LocalDTO


async def create_account(new_account: CreateAccount):

    data = validate_new_account(new_account=new_account)
    local_dto = LocalDTO()
    local_dto.error = []

    if data:  # TODO: Mejorar código response con datos no válidos
        local_dto.error = data
        return local_dto.__dict__

    firebase_api_client = FirebaseIntegrationApiClient()
    manager = new_account.legal_representative[0]

    uid = await firebase_api_client.create_account(email=manager["email"], password=manager["password"])

    if type(uid) == int: # TODO: Mejorar código response con error firebase credenciales
        local_dto.error = "No se puede crear credenciales"

    ms_local = MSLocalClient()

    branch = dict(new_account.branch)
    branch["uid"] = uid

    del (manager["password"])
    owner = new_account.legal_representative[1]

    new_account_dict = {
        "legal_representative": [manager, owner],
        "branch": branch,
        "restaurant": new_account.restaurant.dict(),
        "bank_restaurant": new_account.bank_restaurant.dict()
    }

    new_local_id = await ms_local.create_account(new_account=new_account_dict)

    if not new_local_id:  # TODO: Mejorar respuesta registro de sucursal
        local_dto.error = "Error al registrar datos de sucursal"
        if type(uid) == str:
            await firebase_api_client.delete_account(uid)

    local_dto.data = new_local_id
    return local_dto.__dict__


def define_response(data):  # TODO:  Crear funcion para crear respuesta estandar
    logger.info("data: {}", data)
    pass


