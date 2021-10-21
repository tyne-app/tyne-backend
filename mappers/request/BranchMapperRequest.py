from loguru import logger
from dto.request.local_request_dto import Branch
from repository.entity.BranchEntity import BranchEntity
from dto.dto import GenericDTO as wrapperDTO


class BranchMapperRequest:

    def to_branch_entity(self, branch: Branch, branch_geocoding: dict, uid: str):
        logger.info("branch: {}, branch_geocoding: {}, uid: {}", branch, branch_geocoding, uid)
        branch_dict = branch.dict()
        del(branch_dict['name'])

        branch_entity = BranchEntity(**branch_dict)
        branch_entity.latitude = branch_geocoding['latitude']
        branch_entity.longitude = branch_geocoding['longitude']
        branch_entity.uid = uid
        branch_entity.is_active = True

        return branch_entity

    def to_branch_create_response(self, body=None):
        response = wrapperDTO()
        if not body:
            response.data = [{"message": "Local creado correctamente"}]
        else:
            response.data = [{'message': body}]

        return response.__dict__
