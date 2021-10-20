from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class RestaurantImageEntity(Base):
    __tablename__ = "restaurant_image"
    __table_args__ = {'schema': 'tyne'}
    id = Column(Integer, primary_key = True,index = True)
    url_image = Column(String)

    restaurant_id = Column(Integer, ForeignKey("tyne.restaurant.id"))
