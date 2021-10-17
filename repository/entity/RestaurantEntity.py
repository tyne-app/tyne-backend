from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.StateEntity import StateEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.RestaurantImageEntity import RestaurantImageEntity


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

    branches = relationship("BranchEntity", back_populates='restaurant')
    restaurant_images = relationship("RestaurantImageEntity", back_populates="restaurant")
