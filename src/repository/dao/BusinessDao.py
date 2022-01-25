from src.repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from src.repository.entity.UserEntity import UserEntity
from src.repository.entity.RestaurantEntity import RestaurantEntity
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from fastapi import status


class BusinessDao:
    _throwerExceptions = ThrowerExceptions()

    MANAGER_EXIST = "Encargado ya existe en el sistema"
    LEGAL_REPRESENTATIVE_EXIST = "Representante legal ya existe en el sistema"
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
        legal_representative_exist = db.query(LegalRepresentativeEntity) \
            .filter(LegalRepresentativeEntity.identifier == identifier.identifier) \
            .first()
        if legal_representative_exist:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=[self.LEGAL_REPRESENTATIVE_EXIST],
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
