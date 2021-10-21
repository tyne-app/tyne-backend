import json
import os
from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger
from exception.exceptions import CustomError

load_dotenv()


class IntegrationService:

    def __init__(self):
        self.validate_token_url = os.getenv('VALIDATE_TOKEN_URL')
        self.login_url = ''
        self.token_data_url = os.getenv('TOKEN_DATA_URL')

    async def validate_token(self, token: str):
        async with AsyncClient() as client:
            try:
                authorization_header = {'Authorization': token}
                response = await client.post(headers=authorization_header, url=self.validate_token_url)

                data = json.loads(response.text)

                if response.status_code != status.HTTP_200_OK:  # TODO: Mejorar manejo respuesta
                    logger.error('response: {}', response)
                    logger.error('response.text: {}', response.text)
                    raise CustomError(name="Error token no válido",
                                      detail=data['error'],
                                      status_code=response.status_code,
                                      cause="Usuario no autorizado")  # TODO: Llenar campo

                logger.info('response: {}', response)
                logger.info('response.text: {}', response.text)

                return True
            except RequestError as error:
                logger.error('error: {}', error)
                logger.error('error.args: {}', error.args)
                raise CustomError(name="Error conexión con ms integración",
                                  detail=error.args[0],
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  cause="No se puede validar token")  # TODO: Llenar campo