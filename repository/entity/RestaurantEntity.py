from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.StateEntity import StateEntity


class RestaurantEntity(Base):
    __tablename__ = "restaurant"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(100))
    name = Column(String(100))
    created_date = Column(TIMESTAMP)
    social_reason = Column(String(200))
    commercial_activity = Column(String(100))
    phone = Column(String(15))

    # FK
    # legal_representative_id = Column(Integer, ForeignKey('tyne.legal_representative.id'))
    # legal_representative = relationship("LegalRepresentativeEntity")
    # state_id = Column(Integer, ForeignKey('tyne.state.id'))
    # state = relationship("StateEntity")

    # Back FK
    # restaurant_branch = relationship("BranchEntity", back_populates='restaurant')
