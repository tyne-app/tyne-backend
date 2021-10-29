from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity


class ReservationEntity(Base):
    __tablename__ = "reservation"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    reservation_date = Column(TIMESTAMP)
    preference = Column(String(50))
    people = Column(Integer)
    payment_id = Column(String(100))

    client_id = Column(Integer, ForeignKey('tyne.client.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    opinion_reservation = relationship("OpinionEntity", back_populates='reservation')
    # reservation_change_status: list[ReservationChangeStatusEntity] = relationship("ReservationChangeStatusEntity", back_populates='reservation')
