from sqlalchemy import Integer, String, Column

from src.configuration.database.database import Base


class CountryEntity(Base):
    __tablename__ = 'country'
    __table_args__ = {"schema": "tyne"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
