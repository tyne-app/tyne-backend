from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP

from configuration.database.database import Base


class ScheduleEntity(Base):
    __tablename__ = "schedule"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    opening_hour = Column(TIMESTAMP)
    closing_hour = Column(TIMESTAMP)
    is_monday = Column(Boolean)
    is_tuesday = Column(Boolean)
    is_wednesday = Column(Boolean)
    is_thursday = Column(Boolean)
    is_friday = Column(Boolean)
    is_saturday = Column(Boolean)
    is_sunday = Column(Boolean)

    # Back FK
    # branch_schedule = relationship("Branch", back_populates='schedule')
