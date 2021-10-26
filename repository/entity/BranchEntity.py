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
    latitude = Column(DECIMAL)
    longitude = Column(DECIMAL)
    street_number = Column(Integer)

    state_id = Column(Integer, ForeignKey('tyne.state.id'))
    restaurant_id = Column(Integer, ForeignKey('tyne.restaurant.id'))
    branch_bank_id = Column(Integer, ForeignKey('tyne.branch_bank.id'))
    manager_id = Column(Integer, ForeignKey('tyne.manager.id'))

    product_branch = relationship("ProductEntity", back_populates='branch')
    manager = relationship("ManagerEntity", back_populates='branch')