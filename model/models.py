from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP, Float
from sqlalchemy.orm import relationship

from database.config import Base


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, )
    description = Column(String)
    category_id = Column(Integer)
    branch_id = Column(Integer)

    items = relationship("Item", back_populates="owner")


class Branch(Base):
    __tablename__ = "branch"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    accept_pet = Column(Boolean, default=False)
    description = Column(String)
    legal_representative_id = Column(Integer)
    state_id = Column(Integer)
    restaurant_id = Column(Integer)
    bank_restaurant_id = Column(Integer)
    street = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    uid = Column(String)
    state = Column(Boolean, default=True)
    street_number = Column(Integer)

    items = relationship("Item", back_populates="owner")
