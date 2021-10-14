from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.TypeLegalRepresentativeEntity import TypeLegalRepresentativeEntity
from repository.entity.RestaurantEntity import RestaurantEntity


class LegalRepresentativeEntity(Base):
    __tablename__ = "legal_representative"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    last_name = Column(String(100))
    identifier = Column(String(100))
    email = Column(String(100))
    phone = Column(String(100))

    # FK
    type_legal_representative_id = Column(Integer, ForeignKey('tyne.type_legal_representative.id'), nullable=True)

    # Back FK
    type_legal_representative = relationship('TypeLegalRepresentativeEntity', back_populates='representative_legal')
    # legalrepresentative_branch = relationship("BranchEntity", back_populates='legal_representative')

    # type_legal_representative = relationship("TypeLegalRepresentative",back_populates="represent")
    # type_legal_representative = relationship("TypeLegalRepresentative")
