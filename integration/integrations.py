import os

from httpx import AsyncClient, RequestError, HTTPStatusError
from schema.local_schemas import CreateAccountMSLocal
from fastapi import status
import json
from dotenv import load_dotenv


# TODO: Variables a eliminar corto plazo
CREATE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login"
VALIDATE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login/validate"
DELETE_ACCOUNT_INTEGRATION = "https://ms-integration-apis.herokuapp.com/v1/login"

CREATE_ACCOUNT_LOCAL = "http://localhost:8000/v1/local/register"
DELETE_ACCOUNT_LOCAL = "http://localhost:8000/v1/local/delete"

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
                print(response)
                if response.status_code != status.HTTP_200_OK:
                    return status.HTTP_400_BAD_REQUEST

                data = json.loads(response.text)
                return data["data"]["uid"]

            except RequestError as exc:

                return status.HTTP_500_INTERNAL_SERVER_ERROR

    async def delete_account(self, uid: str):
        async with AsyncClient() as client:
            try:
                delete_account_url = self.delete_account_integration + "/" + uid
                response = await client.delete(url=delete_account_url)
                if response.status_code != 200:
                    return status.HTTP_400_BAD_REQUEST
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
                print("RESPONSE MS")
                print(response)
                print(response.text)
                if response.status_code != status.HTTP_201_CREATED:
                    return None

                data = json.loads(response.text)
                print("DATA")
                print(data)
                print(type(data))

                return int(data["data"])

            except RequestError as exc:
                return None

    async def delete_account(self, branch_id):  # TODO: Completar url con branch id
        async with AsyncClient() as client:
            try:
                response = await client.delete(url=self.delete_account_local)
                print("RESPONSE DLETE MS")
                print(response)
                print(response.text)
                return True
            except RequestError as exc:
                return status.HTTP_500_INTERNAL_SERVER_ERROR

