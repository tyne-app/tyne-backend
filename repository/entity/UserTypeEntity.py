from sqlalchemy import Integer, String, Column
from configuration.database.database import Base


class UserTypeEntity(Base):
    __tablename__ = "user_type"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))