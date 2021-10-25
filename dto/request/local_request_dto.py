from pydantic import BaseModel
from typing import Optional
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchBankEntity import BranchBankEntity
from dto.dto import GenericDTO as wrapperDTO




class Manager(BaseModel):
    name: str
    last_name: str
    phone: str
    email: str
    password: str


class LegalRepresentative(BaseModel):
    name: str
    last_name: str
    identifier: str
    email: str
    phone: str


class Restaurant(BaseModel):
    identifier: str
    social_reason: str
    commercial_activity: str
    phone: str
    street: str
    street_number: int
    state_id: int


class Branch(BaseModel):
    name: Optional[str]
    street: str
    street_number: int
    state_id: int
    accept_pet: bool


class BranchBank(BaseModel):
    account_holder_identifier: str
    account_holder_name: str
    account_number: str
    account_type: str
    bank_id: int


class ParserDTO:

    def to_manager_entity(self, manager: Manager):
        manager_dict = manager.dict()
        del (manager_dict['password'])
        manager_entity = ManagerEntity(**manager_dict)
        return manager_entity

    def to_legal_representative_entity(self, legal_representative: LegalRepresentative):
        legal_representative_entity = LegalRepresentativeEntity(**legal_representative.dict())
        return legal_representative_entity

    def to_restaurant_entity(self, restaurant: Restaurant, name: str):
        restaurant_entity = RestaurantEntity(**restaurant.dict())
        restaurant_entity.name = name

        return restaurant_entity

    def to_branch_entity(self, branch: Branch, branch_geocoding: dict, uid: str):
        branch_dict = branch.dict()
        del (branch_dict['name'])

        branch_entity = BranchEntity(**branch_dict)
        branch_entity.latitude = branch_geocoding['latitude']
        branch_entity.longitude = branch_geocoding['longitude']
        branch_entity.uid = uid
        branch_entity.is_active = True

        return branch_entity

    def to_branch_bank_entity(self, branch_bank: BranchBank):
        branch_bank_entity = BranchBankEntity(**branch_bank.dict())
        return branch_bank_entity

    def to_branch_create_response(self, content: any):
        response = wrapperDTO()
        response.data = [{'message': content}]
        return response.__dict__


class NewAccount(BaseModel, ParserDTO):
    manager: Manager
    legal_representative: LegalRepresentative
    restaurant: Restaurant
    branch: Branch
    branch_bank: BranchBank


class NewBranch(BaseModel, ParserDTO):
    manager: Manager
    branch: Branch
    branch_bank: BranchBank


