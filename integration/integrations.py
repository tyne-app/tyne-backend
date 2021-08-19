import http

class IntegrationApi:
    CREATE_ACCOUNT = "https://ms-integration-apis.herokuapp.com/v1/login"  # TODO: ES POST
    VALIDATE_ACCOUNT = "https://ms-integration-apis.herokuapp.com/v1/login/validate"  # TODO: Es GET
    DELETE_ACCOUNT = "https://ms-integration-apis.herokuapp.com/v1/login"  # TODO: Es DELETE

    async def request(self):
        # TODO:
        pass