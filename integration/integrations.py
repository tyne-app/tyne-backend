import os
from httpx import AsyncClient, RequestError
from schema import local_schemas, search_schema
from fastapi import status
import json
from loguru import logger
from dotenv import load_dotenv


# TODO: Variables a eliminar corto plazo
# TODO: DEFINIR CONSTANTES CON VERIONES DE API, EJ CREATE_ACCOUNT_URL_V1
CREATE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login"
VALIDATE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login/validate"
DELETE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login"
SEARCH_ALL_BRANCH = ""
SEARCH_ALL_BRANCH_BY_CLIENT = ""

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


class MSLocalClient:
    def __init__(self):
        self.create_account_local = os.getenv('CREATE_ACCOUNT_LOCAL')
        self.delete_account_local = os.getenv('DELETE_ACCOUNT_LOCAL')
        self.search_all = os.getenv('SEARCH_ALL_BRANCH')
        self.search_branch = os.getenv('SEARCH_BRANCH')

    async def create_account(self, new_account: local_schemas.CreateAccountMSLocal):
        async with AsyncClient() as client:
            try:
                response = await client.post(url=self.create_account_local, json=new_account)

                logger.info("response: {}", response)
                logger.info("response.text: {}", response.text)

                data = json.loads(response.text)

                if response.status_code != status.HTTP_201_CREATED:
                    logger.error("response: {}", response)
                    logger.error("response.text: {}", response.text)
                    return data['error']

                return int(data["data"])

            except RequestError as exception:
                logger.error("Exception: {}", exception)
                logger.error("response.text: {}", exception)
                return f"Excepción: {exception.response} - {exception.respose.status_code}"

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

    async def search_branch_profile(self, branch_id: int):
        async with AsyncClient() as client:
            try:
                search_branch_profile_url = self.search_branch + "/" + str(branch_id)
                logger.info('search_branch_profile_url: {}', search_branch_profile_url)
                response = await client.get(url=search_branch_profile_url)
                logger.info("response: {}", response)
                logger.info("response.text: {}", response.text)

                data = json.loads(response.text)

                if response.status_code != status.HTTP_200_OK:
                    logger.error("response: {}", response)
                    logger.error("response.text: {}", response.text)
                    return data['error']

                return data["data"]

            except RequestError as exception:
                logger.error("Exception: {}", exception)
                logger.error("response.text: {}", exception)
                return f"Excepción: {exception.response} - {exception.respose.status_code}"

    async def search_all_branch(self, search_parameters: dict, client_id: int):
        async with AsyncClient() as client:
            try:
                search_url = self.search_all + (f"/{client_id}" if client_id else '')
                logger.info('search_url: {}', search_url)
                response = await client.post(url=search_url, json=search_parameters)
                print(response)
                print(response.text)
                if response.status_code != status.HTTP_200_OK:
                    logger.error("response.text: {}", response.text)
                    return None  # RETORNAR ERROR Y RETORNAR RESPUESTA AMIGABLE
                data = json.loads(response.text)
                return data['data']
            except RequestError as exc:
                print(exc)
                print(exc.args)
                return None


class MapBoxIntegrationClient:

    def __init__(self):
        self.coordinates_url = os.getenv('MAPBOX_URL')

    async def get_latitude_longitude(self, address: str):
        async with AsyncClient() as client:
            try:
                mapbox_url = self.coordinates_url + "/" + address
                logger.info("mapbox_url: {}", mapbox_url)

                response = await client.get(url=mapbox_url)
                logger.info("response: {}", response)
                logger.info("response.text: {}", response.text)

                if response.status_code != status.HTTP_200_OK:
                    logger.error("response: {}", response)
                    logger.error("response.text: {}", response.text)
                    return None
                data = json.loads(response.text)
                logger.info("data: {}", data)

                if 'data' not in data:
                    return None

                return data["data"]
            except RequestError as exc:
                # TODO: Agregar logger
                print(exc)
                print(exc.args)
                return None


class MSIntegrationApi:

    def __init__(self):
        self.validate_token_url = os.getenv('VALIDATE_TOKEN_URL')
        self.login_url = ''
        self.token_data_url = os.getenv('TOKEN_DATA_URL')

    async def validate_token(self, client_token: str):
        async with AsyncClient() as client:
            try:
                authorization_header = { 'Authorization': client_token}
                return await client.post(headers=authorization_header, url=self.validate_token_url)
            except RequestError as exc:
                print(exc)
                print(exc.args)
                return None