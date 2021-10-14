from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base

# from repository.entity.TypeLegalRepresentativeEntity import TypeLegalRepresentativeEntity


class TypeLegalRepresentativeEntity(Base):
    __tablename__ = "type_legal_representative"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    # Back FK
    representative_legal = relationship("LegalRepresentativeEntity", back_populates='type_legal_representative')
    # represent = relationship('LegalRepresentative',backref='legal_representative_lookup')
