from loguru import logger
from dto.request.local_request_dto import BranchBank
from repository.entity.BranchBankEntity import BranchBankEntity


class BranchBankMapperRequest:

    def to_branch_bank_entity(self, branch_bank: BranchBank):
        logger.info('branch_bank: {}', branch_bank)

        branch_bank_entity = BranchBankEntity(**branch_bank.dict())
        return branch_bank_entity

