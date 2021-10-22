from typing import Optional, Union
from pydantic import BaseModel





class LegalRepresentative(BaseModel):
    name: str
    last_name: str
    identifier: str
    email: str
    phone: str





class BankRestaurant(BaseModel):
    account_holder_identifier: str
    account_holder: str
    account_number: str
    account_type: str
    bank_id: int


class LocalOutput(BaseModel):
    data: Optional[int] = []
    error: Optional[str] = []


class CreateAccountMSLocal(BaseModel):
    legal_representative: LegalRepresentative
   # branch: Branch
    #restaurant: Restaurant
    bank_restaurant: BankRestaurant


class Output(BaseModel):
    data: Optional[Union[dict, int]] = []
    error: Optional[Union[dict, int, str]] = []


class LegalRepresentativeOutput(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    phone: str


class BranchOutput(BaseModel):
    id: int
    name: str
    accept_pet: bool
    commercial_activity: str
    description: Optional[str]
    street: str
    street_number: int
    state: str


class BranchProfile(BaseModel):
    legal_representative: LegalRepresentativeOutput
    branch: BranchOutput
    schedule_list: list


class BranchProfileLoginOutput(BaseModel):
    data: Optional[Union[BranchProfile, list]] = []
    error: Optional[Union[str, dict, list]] = []


class BranchPreLogin(BaseModel):
    id: int
    uid: str
    name: str
    accept_pet: bool
    commercial_activity: str
    description: Optional[str]
    street: str
    street_number: int


class BranchProfilePreLoginOutput(BaseModel):
    data: Optional[Union[BranchPreLogin, list]] = []
    error: Optional[Union[str, dict, list]] = []


class NewBranch(BaseModel):
    street: str
    street_number: int
    state_id: int
    accept_pet: bool


class AddBranch(BaseModel):
#    legal_representative: Manager
    new_branch: NewBranch
    bank_restaurant: BankRestaurant


class NewBranchOutput(BaseModel):
    data: Optional[int] = []
    error: Optional[str] = []
