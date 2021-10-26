from datetime import date

from repository.entity.ClientEntity import ClientEntity


class ClientResponse:
    id: int
    name: str
    last_name: str
    birth_date: date
    phone: str
    email: str
    image_url: str

    @classmethod
    def map(cls, client_entity: ClientEntity):
        response = ClientResponse()
        response.id = client_entity.id
        response.name = client_entity.name
        response.last_name = client_entity.last_name
        response.birth_date = client_entity.birth_date
        response.phone = client_entity.phone
        response.email = client_entity.user.email
        response.image_url = client_entity.user.image_url
        return response

