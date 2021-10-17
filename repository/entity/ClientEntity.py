from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class ClientEntity(Base):
    __tablename__ = "client"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(TIMESTAMP)
    email = Column(String(100))
    phone = Column(String(15))
    created_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)
    status = Column(Boolean)
    uid = Column(String(255))
    url_image = Column(String)
