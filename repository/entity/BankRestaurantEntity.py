from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.BankEntity import BankEntity


class BankRestaurantEntity(Base):
    __tablename__ = "bank_restaurant"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    account_holder = Column(String(100))
    account_number = Column(String(100))
    account_type = Column(String(50))

    # FK
    bank_id = Column(Integer, ForeignKey('tyne.bank.id'))

    # Back FK
    bank = relationship('BankEntity', back_populates='restaurants_banks')

