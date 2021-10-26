from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class OpinionEntity(Base):
    __tablename__ = "opinion"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String(100))
    qualification = Column(Integer)
    creation_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)
    client_id = Column(Integer, ForeignKey('tyne.client.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))
    reservation_id = Column(Integer, ForeignKey('tyne.reservation.id'))

    # branch = relationship("BranchEntity", back_populates='opinion_branch')
