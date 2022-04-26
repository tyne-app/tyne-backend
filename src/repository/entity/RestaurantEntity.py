from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.configuration.database.database import Base


class RestaurantEntity(Base):
    __tablename__ = "restaurant"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(100))
    created_date = Column(TIMESTAMP)
    social_reason = Column(String(200))
    commercial_activity = Column(String(100))
    phone = Column(String(15))
    street = Column(String(100))
    street_number = Column(Integer)
    state_id = Column(Integer, ForeignKey('tyne.state.id'))
    legal_representative_id = Column(Integer, ForeignKey('tyne.legal_representative.id'))
    description = Column(String(300))

    branch = relationship("BranchEntity", back_populates='restaurant')
