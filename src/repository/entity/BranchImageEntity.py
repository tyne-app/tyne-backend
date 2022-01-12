from sqlalchemy import Integer, String, Column, ForeignKey, Boolean

from src.configuration.database.database import Base


class BranchImageEntity(Base):
    __tablename__ = "branch_image"
    __table_args__ = {'schema': 'tyne'}
    id = Column(Integer, primary_key=True, index=True)
    url_image = Column(String)
    branch_id = Column(Integer, ForeignKey("tyne.branch.id"))
    is_main_image = Column(Boolean)
