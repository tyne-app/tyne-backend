from pydantic import BaseModel
from typing import Optional, Union


class User(BaseModel):
    email: str
    password: str


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


class NewAccount(BaseModel):
    manager: Manager
    legal_representative: LegalRepresentative
    restaurant: Restaurant
    branch: Branch
    branch_bank: BranchBank


class NewBranch(BaseModel):
    manager: Manager
    branch: Branch
    branch_bank: BranchBank


class SearchParameter(BaseModel):

    name: Optional[str] = None
    dateReservation: Optional[str] = None
    stateId: Optional[int] = None
    sortBy: Optional[Union[int, str]] = None
    orderBy: Optional[Union[int, str]] = None
