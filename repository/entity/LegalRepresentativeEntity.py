from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class LegalRepresentativeEntity(Base):
    __tablename__ = "legal_representative"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    last_name = Column(String(100))
    identifier = Column(String(100))
    email = Column(String(100))
    phone = Column(String(100))
