from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class ReservationEntity(Base):
    __tablename__ = "reservation"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    reservation_date = Column(TIMESTAMP)
    status = Column(String(50))
    created_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)
    preference = Column(String(50))
    people = Column(Integer)

    client_id = Column(Integer, ForeignKey('tyne.client.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))
