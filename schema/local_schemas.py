from pydantic import BaseModel
from typing import Optional, Union


class Owner(BaseModel):
    name: str
    last_name: str
    identifier: str
    email: str
    phone: str
    email: str
    type_legal_representative_id: int


class Manager(BaseModel):
    name: str
    last_name: str
    email: str
    phone: str
    password: str
    type_legal_representative_id: int


class LegalRepresentative(BaseModel):
    name: str
    last_name: str
    identifier: str
    email: str
    phone: str


class Branch(BaseModel):
    name: str
    accept_pet: bool
    commercial_activity: str
    address: str
    state_id: int


class Restaurant(BaseModel):
    identifier: str # TODO: Eliminar columna
    name: str
    address: str  # TODO: Eliminar columna
    state_id: int


class BankRestaurant(BaseModel):
    account_holder_identifier: str
    account_holder: str
    account_number: str
    account_type: str
    bank_id: int


class CreateAccount(BaseModel):
    legal_representative: list
    branch: Branch
    restaurant: Restaurant
    bank_restaurant: BankRestaurant


class LocalOutput(BaseModel):
    data: Optional[int] = []
    error: Optional[str] = []
# TODO: Agregar esquemas con actualización datos locales

# TODO: Agregar esquemas con actualización datos bancarios

# TODO: Agregar esquemas con actualización de imágenes de local

# TODO: Esquemas para integraciones
class CreateAccountMSLocal(BaseModel):
    legal_representative: LegalRepresentative
    branch: Branch
    restaurant: Restaurant
    bank_restaurant: BankRestaurant


class Output(BaseModel):
    data: Optional[Union[dict, int]] = []
    error: Optional[Union[dict, int, str]] = []

