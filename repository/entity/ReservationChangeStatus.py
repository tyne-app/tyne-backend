from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP

from configuration.database.database import Base


class ReservationChangeStatus(Base):
    __tablename__ = "reservation_change_status"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    status_id = Column(Integer, ForeignKey('tyne.reservation_status.id'))
    datetime = Column(TIMESTAMP)
    reservation_id = Column(Integer, ForeignKey('tyne.reservation.id'))
