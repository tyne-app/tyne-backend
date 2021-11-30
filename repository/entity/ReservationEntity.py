from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP, Date
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class ReservationEntity(Base):
    __tablename__ = "reservation"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    reservation_date = Column(Date)
    preference = Column(String(50))
    people = Column(Integer)
    payment_id = Column(String(100))
    hour = Column(String(5))
    transaction_id = Column(String(50))

    client_id = Column(Integer, ForeignKey('tyne.client.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    opinion_reservation = relationship("OpinionEntity", back_populates='reservation')
    reservation_change_status = relationship("ReservationChangeStatusEntity", back_populates='reservation')
