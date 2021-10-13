from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class BranchEntity(Base):
    __tablename__ = "branch"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    accept_pet = Column(Boolean)
    commercial_activity = Column(String(100))
    description = Column(String(100))
    address = Column(String(100))
    longitud = Column(DECIMAL)
    latitud = Column(DECIMAL)

    # FK
    legal_representative_id = Column(Integer, ForeignKey('tyne.legal_representative.id'))
    restaurant_id = Column(Integer, ForeignKey('tyne.restaurant.id'))
    state_id = Column(Integer, ForeignKey('tyne.state.id'))
    bank_restaurant_id = Column(Integer, ForeignKey('tyne.bank_restaurant.id'))
    # schedule_id = Column(Integer, ForeignKey('tyne.schedule.id'))

    legal_representative = relationship("LegalRepresentative", back_populates='legalrepresentative_branch')
    restaurant = relationship("Restaurant", back_populates='restaurant_branch')
    state = relationship("State", foreign_keys='[Branch.state_id]')
    bank_restaurant = relationship("BankRestaurant", foreign_keys='[Branch.bank_restaurant_id]')

    # Back FK
    # menu_branch = relationship("Menu", back_populates='branch')
    # product_branch = relationship("ProductEntity", back_populates='branch')
    # children = relationship("product", lazy='joined')
