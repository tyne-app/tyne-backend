from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base

from repository.entity.BranchEntity import BranchEntity
from repository.entity.ScheduleEntity import ScheduleEntity


class BranchScheduleEntity(Base):
    __tablename__ = "branch_schedule"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))
    schedule_id = Column(Integer, ForeignKey('tyne.schedule.id'))
