from fastapi import status

from dto.dto import GenericDTO as ValidatorDTO
from integration.integrations import MSIntegrationApi

MSG_UNAUTHORIZED = "Usuario no autorizado"


async def validate_token(client_token: str):
    validator_dto = ValidatorDTO()
    ms_integration_api = MSIntegrationApi()

    response = await ms_integration_api.validate_token(client_token=client_token)
    # validated_token = json.loads(response.text) # TODO: Parece que devuelve true si es correcto. Agregar a validacion

    if response.status_code != status.HTTP_200_OK:
        validator_dto.error = MSG_UNAUTHORIZED

    return validator_dto.__dict__