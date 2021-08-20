import logging
import os
from httpx import AsyncClient, RequestError
from schema.local_schemas import CreateAccountMSLocal
from fastapi import status
import json
from loguru import logger
from dotenv import load_dotenv


# TODO: Variables a eliminar corto plazo
CREATE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login"
VALIDATE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login/validate"
DELETE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login"

CREATE_ACCOUNT_LOCAL = "http://localhost:8000/v1/local/register"
DELETE_ACCOUNT_LOCAL = "http://localhost:8000/v1/local/delete"

MAPBOX_URL = "https://ms-integration-apis.herokuapp.com/v1/mapbox/getLatitudeLongitude"

load_dotenv()


class FirebaseIntegrationApiClient:

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
                if response.status_code != status.HTTP_200_OK:
                    logger.error("response.text: {}", response.text)
                    return None
                logger.info("response.text: {}", response.text)
                data = json.loads(response.text)
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


class MSLocalClient:

    def __init__(self):
        self.create_account_local = os.getenv('CREATE_ACCOUNT_LOCAL')
        self.delete_account_local = os.getenv('DELETE_ACCOUNT_LOCAL')

    async def create_account(self, new_account: CreateAccountMSLocal):
        async with AsyncClient() as client:
            try:
                response = await client.post(url=self.create_account_local, json=new_account)

                if response.status_code != status.HTTP_201_CREATED:
                    logger.error("response.text: {}", response.text)
                    return None
                logger.info("response.text: {}", response.text)
                data = json.loads(response.text)
                return int(data["data"])

            except RequestError as exc:
                return None

    async def delete_account(self, branch_id: int):
        async with AsyncClient() as client:
            try:
                delete_url = self.delete_account_local + "/" + branch_id # TODO: Tal vez de error al ser int
                response = await client.delete(url=delete_url)
                print("RESPONSE DLETE MS")
                print(response)
                print(response.text)
                return True
            except RequestError as exc:
                return None


class MapBoxIntegrationClient:

    def __init__(self):
        self.coordinates_url = os.getenv('MAPBOX_URL')

    async def get_latitude_longitude(self, address: str):
        async with AsyncClient() as client:
            try:
                mapbox_url = self.coordinates_url + "/" + address
                response = await client.get(url=mapbox_url)
                if response.status_code != status.HTTP_200_OK:
                    return None
                data = json.loads(response.text)
                return data["data"]
            except RequestError as exc:
                # TODO: Agregar logger
                return None