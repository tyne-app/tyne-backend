from sqlalchemy import Integer, Column, ForeignKey

from configuration.database.database import Base


class BranchScheduleEntity(Base):
    __tablename__ = "branch_schedule"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))
    schedule_id = Column(Integer, ForeignKey('tyne.schedule.id'))
