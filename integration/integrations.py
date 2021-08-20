from httpx import AsyncClient, RequestError, HTTPStatusError
from schema.local_schemas import CreateAccountMSLocal
from fastapi import status
import json


class FirebaseIntegrationApiClient:
    CREATE_ACCOUNT = "https://ms-integration-apis.herokuapp.com/v1/login"  # TODO: ES POST evitar código hardcodeado
    VALIDATE_ACCOUNT = "https://ms-integration-apis.herokuapp.com/v1/login/validate"  # TODO: Es GET
    DELETE_ACCOUNT = "https://ms-integration-apis.herokuapp.com/v1/login"  # TODO: Es DELETE

    async def create_account(self, email: str, password: str):
        async with AsyncClient() as client:
            credentials = {
                "email": email,
                "password": password
            }
            try:
                response = await client.post(url="https://ms-integration-apis.herokuapp.com/v1/login", json=credentials)
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
                delete_account_url = self.DELETE_ACCOUNT + "/" + uid
                response = await client.delete(url=delete_account_url)
                if response.status_code != 200:
                    return status.HTTP_400_BAD_REQUEST
                return True  # TODO: Cambiar parámetro
            except RequestError as exc:
                return status.HTTP_500_INTERNAL_SERVER_ERROR


class MSLocalClient:
    CREATE_ACCOUNT = "http://localhost:8000/v1/local/register"
    DELETE_ACCOUNT = "http://localhost:8000/v1/local/delete"

    async def create_account(self, new_account: CreateAccountMSLocal):
        async with AsyncClient() as client:
            try:
                response = await client.post(url=self.CREATE_ACCOUNT, json=new_account)
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

    async def delete_account(self, branch_id):
        async with AsyncClient() as client:
            try:
                response = await client.delete(url=self.DELETE_ACCOUNT)
                print("RESPONSE DLETE MS")
                print(response)
                print(response.text)
                return True
            except RequestError as exc:
                return status.HTTP_500_INTERNAL_SERVER_ERROR

