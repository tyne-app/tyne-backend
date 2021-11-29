from datetime import datetime

from pydantic import BaseModel
from starlette import status

from enums.UserTypeEnum import UserTypeEnum
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions
from validator.UtilsValidator import UtilsValidator


class ClientSocialRegistrationRequest(BaseModel):
    name: str
    lastName: str
    email: str
    token: str

    _utils_validator_ = UtilsValidator()
    _throwerExceptions = ThrowerExceptions()

    def to_client_entity(self, user: UserEntity):
        entity = ClientEntity()
        entity.name = self.name
        entity.last_name = self.lastName
        entity.birth_date = None
        entity.phone = None
        entity.created_date = datetime.now()
        entity.update_date = datetime.now()
        entity.user = user
        return entity

    def to_user_entity(self, image_url: str, password: str):
        entity = UserEntity()
        entity.created_date = datetime.now()
        entity.password = password
        entity.is_active = True
        entity.id_user_type = int(UserTypeEnum.cliente.value)
        entity.email = self.email
        entity.image_url = image_url
        return entity

    async def validate_fields(self):
        invalid_data = {}

        if not self._utils_validator_.validate_not_empty(self.name):
            invalid_data["name"] = self._utils_validator_.INVALID_DATA_MESSAGE

        if not self._utils_validator_.validate_not_empty(self.lastName):
            invalid_data["lastName"] = self._utils_validator_.INVALID_DATA_MESSAGE

        if not self._utils_validator_.validate_not_empty(self.email):
            invalid_data["email"] = self._utils_validator_.INVALID_DATA_MESSAGE

        if not self._utils_validator_.validate_not_empty(self.token):
            invalid_data["token"] = self._utils_validator_.INVALID_DATA_MESSAGE

        if invalid_data:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=invalid_data,
                                                                 status_code=status.HTTP_400_BAD_REQUEST,
                                                                 cause=invalid_data)

        return True
