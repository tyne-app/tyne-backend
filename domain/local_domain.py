from validator.local_validator import validate_new_account
from schema.local_schemas import CreateAccount


def create_account(new_account: CreateAccount):
    data = validate_new_account(new_account=new_account)
    if data:
        return data


    return "OK"
