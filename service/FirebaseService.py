import json
import os

from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger

from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions

load_dotenv()


class FirebaseService:
    _throwerExceptions = ThrowerExceptions()

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
                    await self._throwerExceptions.throw_custom_exception(name=Constants.CREDENTIALS_CREATE_ERROR,
                                                                         detail=Constants.CREDENTIALS_CREATE_ERROR,
                                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                         cause=response.text)

                return data["data"]["uid"]

            except RequestError as error:
                await self._throwerExceptions.throw_custom_exception(name=Constants.CREDENTIALS_CREATE_ERROR,
                                                                     detail=Constants.CREDENTIALS_CREATE_ERROR,
                                                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                     cause=error)

    async def delete_account(self, uid: str):
        async with AsyncClient() as client:
            try:
                delete_account_url = self.delete_account_integration + "/" + uid
                response = await client.delete(url=delete_account_url)
                if response.status_code != 200:
                    await self._throwerExceptions.throw_custom_exception(name=Constants.CREDENTIALS_CREATE_ERROR,
                                                                         detail=Constants.CREDENTIALS_CREATE_ERROR,
                                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                         cause=response.text)
                logger.info("response.text: {}", response.text)
                return True  # TODO: Definir parámetro a retornar
            except RequestError as error:
                await self._throwerExceptions.throw_custom_exception(name=Constants.CREDENTIALS_CREATE_ERROR,
                                                                     detail=Constants.CREDENTIALS_CREATE_ERROR,
                                                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                     cause=error)
