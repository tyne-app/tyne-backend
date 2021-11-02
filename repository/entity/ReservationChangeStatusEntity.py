from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class ReservationChangeStatusEntity(Base):
    __tablename__ = "reservation_change_status"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    status_id = Column(Integer)
    datetime = Column(TIMESTAMP)
    reservation_id = Column(Integer, ForeignKey('tyne.reservation.id'))

    # reservation_status = relationship("ReservationStatusEntity", back_populates='reservation_change_status')
    # reservation = relationship("ReservationEntity", back_populates='reservation_change_status')