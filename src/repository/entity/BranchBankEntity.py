from sqlalchemy import Column, Integer, String, ForeignKey
from src.configuration.database.database import Base


class BranchBankEntity(Base):
    __tablename__ = "branch_bank"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    account_holder_name = Column(String(100))
    account_number = Column(String(100))
    account_type = Column(String(100))
    account_holder_identifier = Column(String(15))

    bank_id = Column(Integer, ForeignKey('tyne.bank.id'))
