from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP

from configuration.database.database import Base


class ClientEntity(Base):
    __tablename__ = "client"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))
    last_name = Column(String(100))
    birth_date = Column(TIMESTAMP)
    phone = Column(String(15))
    created_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)
    id_user = Column(Integer, ForeignKey('tyne.user.id'))
