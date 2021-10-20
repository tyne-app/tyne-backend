import json
import os
from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger
from exception.exceptions import CustomError

load_dotenv()


class FirebaseService:

    def __init__(self):
        self.create_account_integration = os.getenv('CREATE_ACCOUNT_INTEGRATION')
        self.validate_account_integration = os.getenv('VALIDATE_ACCOUNT_INTEGRATION')
        self.delete_account_integration = os.getenv('DELETE_ACCOUNT_INTEGRATION')

    async def create_account(self, email: str, password: str):
        async with AsyncClient() as client:
            credentials = {
                "email": email,
                "password": password
            }
            try:
                response = await client.post(url=self.create_account_integration, json=credentials)

                logger.info("response: {}", response)
                logger.info("response.text: {}", response.text)
                data = json.loads(response.text)

                if response.status_code != status.HTTP_200_OK:
                    logger.error("response.text: {}", response)
                    logger.error("response.text: {}", response.text)
                    raise CustomError(name="Error al crear redenciales",
                                      detail=data['error'],
                                      status_code=response.status_code,
                                      cause="")   # TODO: Llenar campo

                return data["data"]["uid"]

            except RequestError as error:
                logger.error('error: {}', error)
                logger.error('error.args: {}', error.args)
                raise CustomError(name="Error al crear redenciales",
                                  detail=error.args[0],
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  cause="")  # TODO: Llenar campo

    async def delete_account(self, uid: str):
        async with AsyncClient() as client:
            try:
                delete_account_url = self.delete_account_integration + "/" + uid
                response = await client.delete(url=delete_account_url)
                if response.status_code != 200:
                    logger.error("response.text: {}", response.text)
                    raise CustomError(name="Error al crear redenciales",
                                      detail=response.text,
                                      status_code=response.status_code,
                                      cause="")  # TODO: Llenar campo
                logger.info("response.text: {}", response.text)
                return True  # TODO: Definir parámetro a retornar
            except RequestError as error:
                logger.error('error: {}', error)
                logger.error('error.args: {}', error.args)
                raise CustomError(name="Error al crear redenciales",
                                  detail=error.args[0],
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  cause="")  # TODO: Llenar campo
