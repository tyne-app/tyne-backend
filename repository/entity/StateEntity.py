from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class StateEntity(Base):
    __tablename__ = 'state'
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city_id = Column(Integer, ForeignKey('tyne.city.id'))
    city = relationship("CityEntity")

