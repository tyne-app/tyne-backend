from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.configuration.database.database import Base


class UserEntity(Base):
    __tablename__ = "user"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(TIMESTAMP)
    password = Column(String(255))
    is_active = Column(Boolean)
    is_social = Column(Boolean)
    id_user_type = Column(Integer)  # TODO:  Aunque no se ocupa Foreign Key, por ORM se valida igual el valor de este atributo
    email = Column(String(100))
    image_url = Column(String(500))
    image_id = Column(String(200))

    client = relationship("ClientEntity", back_populates='user')
    manager = relationship("ManagerEntity", back_populates='user')
