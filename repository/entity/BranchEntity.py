from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base


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
    manager_id = Column(Integer, ForeignKey('tyne.manager.id'))
    state_id = Column(Integer, ForeignKey('tyne.state.id'))
    restaurant_id = Column(Integer, ForeignKey('tyne.restaurant.id'))
    branch_bank_id = Column(Integer, ForeignKey('tyne.bank_restaurant.id'))
