from sqlalchemy import Integer, String, Column, Boolean
from configuration.database.database import Base


class BankEntity(Base):
    __tablename__ = "bank"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    active = Column(Boolean)
