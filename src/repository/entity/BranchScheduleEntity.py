from sqlalchemy import Integer, Column, ForeignKey, String, Boolean

from src.configuration.database.database import Base


class BranchScheduleEntity(Base):
    __tablename__ = "branch_schedule"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    opening_hour = Column(String(50))
    closing_hour = Column(String(50))
    active = Column(Boolean)
    day = Column(Integer)
