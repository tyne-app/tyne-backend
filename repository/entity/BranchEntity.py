from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.BranchTypeEntity import BranchTypeEntity
from repository.entity.BranchScheduleEntity import BranchScheduleEntity
from repository.entity.ReservationEntity import ReservationEntity
from repository.entity.ProductEntity import ProductEntity
from repository.entity.RestaurantEntity import RestaurantEntity


class BranchEntity(Base):
    __tablename__ = "branch"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    accept_pet = Column(Boolean)
    description = Column(String(100))
    street = Column(String(100))
    longitude = Column(DECIMAL)
    latitude = Column(DECIMAL)
    uid = Column(String(250))
    is_active = Column(Boolean)
    street_number = Column(Integer)

    # FK
    legal_representative_id = Column(Integer, ForeignKey('tyne.legal_representative.id'))
    state_id = Column(Integer, ForeignKey('tyne.state.id'))
    restaurant_id = Column(Integer, ForeignKey('tyne.restaurant.id'))
    branch_type_id = Column(Integer, ForeignKey('tyne.restaurant.id'))
    branch_bank_id = Column(Integer, ForeignKey('tyne.bank_restaurant.id'))

    branch_type = relationship("BranchTypeEntity", back_populates="branches")
    branches_schedules = relationship("BranchScheduleEntity", back_populates="branch")
    reservations = relationship("ReservationEntity", back_populates="reservations")
    products = relationship("ProductEntity", back_populates="branch")
    restaurant = relationship("RestaurantEntity", back_populates="branches")
