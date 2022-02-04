from starlette import status

from src.repository.entity.ManagerEntity import ManagerEntity
from src.repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from src.repository.entity.RestaurantEntity import RestaurantEntity
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.BranchBankEntity import BranchBankEntity
from src.repository.entity.UserEntity import UserEntity
from src.repository.entity.BranchImageEntity import BranchImageEntity
from src.dto.dto import GenericDTO as wrapperDTO
from src.dto.request.business_request_dto import LegalRepresentative
from src.dto.request.business_request_dto import Restaurant
from src.dto.request.business_request_dto import Branch
from src.dto.request.business_request_dto import BranchBank
from src.dto.request.business_request_dto import Manager
from src.dto.response.business_response_dto import PreviewBranch
from src.util.Constants import Constants


class BusinessMapperRequest:

    async def to_manager_entity(self, manager: Manager):
        manager_dict = manager.dict()
        del (manager_dict['email'])
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

    def to_branch_entity(self, branch: Branch, branch_geocoding: dict):
        branch_dict = branch.dict()
        del (branch_dict['name'])

        branch_entity = BranchEntity(**branch_dict)
        branch_entity.latitude = branch_geocoding['latitude']
        branch_entity.longitude = branch_geocoding['longitude']
        branch_entity.is_active = True

        return branch_entity

    def to_branch_bank_entity(self, branch_bank: BranchBank):
        branch_bank_entity = BranchBankEntity(**branch_bank.dict())
        return branch_bank_entity

    def to_user_entity(self, user_dict: dict, id_user_type: int):
        print(user_dict)
        user_dict['id_user_type'] = id_user_type
        user_entity = UserEntity(**user_dict)
        user_entity.is_active = True
        return user_entity

    def to_branch_image_entity(self, default_main_image: str):
        branch_image_entity = BranchImageEntity()
        branch_image_entity.url_image = default_main_image
        branch_image_entity.is_main_image = True
        return branch_image_entity

    def to_branch_create_response(self, content: any = None):
        response = wrapperDTO()
        response.data = content
        return response.__dict__

    def to_search_branches_response(self, content: list[PreviewBranch], total_items: int, page: int,
                                    result_for_page: int):
        response = wrapperDTO()
        response_dict = response.__dict__
        response_dict['total_items'] = total_items
        response_dict['total_items_page'] = result_for_page
        response_dict['page'] = page
        response_dict['data'] = content

        return response_dict
