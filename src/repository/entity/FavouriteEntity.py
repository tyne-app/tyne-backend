from sqlalchemy import Integer, Column, TIMESTAMP, Boolean, ForeignKey

from src.configuration.database.database import Base


class Favourite(Base):
    __tablename__ = "favoourite"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    is_favourite = Column(Boolean)
    creation_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)

    client_id = Column(Integer, ForeignKey("tyne.client.id"))
    restaurant_id = Column(Integer, ForeignKey("tyne.restaurant.id"))
