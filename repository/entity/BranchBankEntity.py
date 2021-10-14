from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.BankRestaurantEntity import BankRestaurantEntity


class BranchBankEntity(Base):
    __tablename__ = "branch_bank"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    account_holder = Column(String(100))
    account_number = Column(String(100))
    account_type = Column(String(100))
    account_holder_identifier = Column(String(15))

    bank_id = Column(Integer, ForeignKey('tyne.bank.id'))

    # Back FK
    branch_bank_branch = relationship("BranchEntity", back_populates='branch_bank')


