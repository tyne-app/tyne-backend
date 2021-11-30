from sqlalchemy import Integer, Column, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class ScheduleEntity(Base):
    __tablename__ = "schedule"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    opening_hour = Column(TIMESTAMP)
    closing_hour = Column(TIMESTAMP)
    day = Column(Integer)
