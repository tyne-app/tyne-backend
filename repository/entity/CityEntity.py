from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class CityEntity(Base):
    __tablename__ = 'city'
    __table_args__ = {"schema": "tyne"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey('tyne.country.id'))