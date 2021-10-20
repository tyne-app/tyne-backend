from loguru import logger
from dto.request.local_request_dto import LegalRepresentative
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity


class LegalRepresentativeMapperRequest:

    def to_legal_representative_entity(self, legal_representative: LegalRepresentative):
        logger.info('legal_representative: {}', legal_representative)

        legal_representative_entity = LegalRepresentativeEntity(**legal_representative.dict())
        return legal_representative_entity
