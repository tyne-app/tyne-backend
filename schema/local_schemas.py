from pydantic import BaseModel
from typing import Optional


# TODO: Agregar esquemas con registro local
class LegalRepresentative(BaseModel):
    name: str
    last_name: str
    identifier: str
    email: str
    phone: str


class Branch(BaseModel):
    name: str  # TODO: Este campo se podría eliminar
    accept_pet: bool
    commercial_activity: str
    address: str  # TODO: Viene desde front campo dirección + número dirección
    state: str  # TODO: Corresponde a nombre comuna, no es necesario campo region ya que por front se valida la relación


class Restaurant(BaseModel):
    identifier: str # TODO: Eliminar columna
    name: str
    address: str  # TODO: Eliminar columna
    state: str


class BankRestaurant(BaseModel):
    account_holder_identifier: str
    account_holder: str
    account_number: str
    account_type: str
    bank: str


class CreateAccount(BaseModel):
    legal_representative: LegalRepresentative
    branch: Branch
    restaurant: Restaurant
    bank_restaurant: BankRestaurant


class LocalOutput(BaseModel):
    data: Optional[int] = []
    error: Optional[str] = []
# TODO: Agregar esquemas con actualización datos locales

# TODO: Agregar esquemas con actualización datos bancarios

# TODO: Agregar esquemas con actualización de imágenes de local
