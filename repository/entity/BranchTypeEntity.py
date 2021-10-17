from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.BranchEntity import BranchEntity


class BranchTypeEntity(Base):
    __tablename__ = "branch_type"
    __table_args__ = {'schema': 'tyne'}
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(6))

    branches = relationship("BranchEntity", back_populates="branch_type")
