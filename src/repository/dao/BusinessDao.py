from src.repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from src.repository.entity.UserEntity import UserEntity
from src.repository.entity.RestaurantEntity import RestaurantEntity
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from fastapi import status
from sqlalchemy import or_


class BusinessDao:
    _throwerExceptions = ThrowerExceptions()

    MANAGER_EXIST = "Encargado ya existe en el sistema"
    LEGAL_REPRESENTATIVE_EXIST_IDENTIFIER = "Rut del representante legal ya existe en el sistema"
    LEGAL_REPRESENTATIVE_EXIST_EMAIL = "Correo del representante legal ya existe en el sistema"
    RESTAURANT_EXIST = "Local ya existe en el sistema"

    async def verify_manager(self, identifier, db):
        manager_exist = db.query(UserEntity) \
            .filter(UserEntity.email == identifier.email) \
            .first()
        if manager_exist:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=[self.MANAGER_EXIST],
                                                                 status_code=status.HTTP_400_BAD_REQUEST)
        return True

    async def verify_legal_representative(self, identifier, db):
        print(identifier)
        data_error = []
        legal_representative_exist = db.query(LegalRepresentativeEntity) \
            .filter(or_(LegalRepresentativeEntity.identifier == identifier.identifier,
                        LegalRepresentativeEntity.email == identifier.email)) \
            .first()

        if legal_representative_exist:
            if legal_representative_exist.identifier == identifier.identifier:
                data_error.append(self.LEGAL_REPRESENTATIVE_EXIST_IDENTIFIER)

            if legal_representative_exist.email == identifier.email:
                data_error.append(self.LEGAL_REPRESENTATIVE_EXIST_EMAIL)

        if data_error:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=data_error,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)

        return True

    async def verify_restaurant(self, identifier, db):
        restaurant_exist = db.query(RestaurantEntity) \
            .filter(RestaurantEntity.identifier == identifier.identifier) \
            .first()
        if restaurant_exist:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=[self.RESTAURANT_EXIST],
                                                                 status_code=status.HTTP_400_BAD_REQUEST)
        return True
