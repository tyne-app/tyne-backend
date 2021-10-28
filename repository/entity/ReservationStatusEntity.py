from sqlalchemy import Column, Integer, String

from configuration.database.database import Base


class ReservationStatusEntity(Base):
    __tablename__ = "reservation_status"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(100))
