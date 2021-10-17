import json
import os

from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger

load_dotenv()


class MSIntegrationApi:

    def __init__(self):
        self.validate_token_url = os.getenv('VALIDATE_TOKEN_URL')
        self.login_url = ''
        self.token_data_url = os.getenv('TOKEN_DATA_URL')

    async def validate_token(self, client_token: str):
        async with AsyncClient() as client:
            try:
                authorization_header = {'Authorization': client_token}
                response = await client.post(headers=authorization_header, url=self.validate_token_url)

                if response.status_code != status.HTTP_200_OK:  # TODO: Mejorar manejo respuesta
                    logger.error('response: {}', response)
                    logger.error('response.text: {}', response.text)

                logger.info('response: {}', response)
                logger.info('response.text: {}', response.text)

                return response
            except RequestError as exc:
                print(exc)
                print(exc.args)
                return None