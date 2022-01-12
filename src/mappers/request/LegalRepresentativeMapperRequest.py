from loguru import logger
from src.dto.request import LegalRepresentative
from src.repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity


class LegalRepresentativeMapperRequest:

    def to_legal_representative_entity(self, legal_representative: LegalRepresentative):
        logger.info('legal_representative: {}', legal_representative)

        legal_representative_entity = LegalRepresentativeEntity(**legal_representative.dict())
        return legal_representative_entity
