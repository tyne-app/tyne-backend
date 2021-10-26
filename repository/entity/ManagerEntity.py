from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class ManagerEntity(Base):
    __tablename__ = "manager"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(100))
    id_user = Column(Integer, ForeignKey('tyne.user.id'))

    branch = relationship("BranchEntity", back_populates='manager')
