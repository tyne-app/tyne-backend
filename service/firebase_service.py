import json
import os

from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger

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
                    logger.error("response.text: {}", response.text)
                    return None

                return data["data"]["uid"]

            except RequestError as exc:
                return None

    async def delete_account(self, uid: str):
        async with AsyncClient() as client:
            try:
                delete_account_url = self.delete_account_integration + "/" + uid
                response = await client.delete(url=delete_account_url)
                if response.status_code != 200:
                    logger.error("response.text: {}", response.text)
                    return None
                logger.info("response.text: {}", response.text)
                return True  # TODO: Cambiar parámetro
            except RequestError as exc:
                return status.HTTP_500_INTERNAL_SERVER_ERROR