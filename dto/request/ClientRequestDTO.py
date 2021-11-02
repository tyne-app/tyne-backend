from datetime import datetime

from pydantic import BaseModel

from repository.entity.ClientEntity import ClientEntity


class ClientRequestDTO(BaseModel):
    name: str
    lastName: str
    birthDate: datetime
    email: str
    phone: str
    password: str

    def to_entity(self, id_login_created):
        entity = ClientEntity()
        entity.name = self.name
        entity.last_name = self.lastName
        entity.birth_date = self.birthDate
        entity.phone = self.phone
        entity.created_date = datetime.now()
        entity.update_date = datetime.now()
        entity.id_user = id_login_created
        return entity
