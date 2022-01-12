from sqlalchemy import Integer, String, Column

from src.configuration.database.database import Base


class TypeCoin(Base):
    __tablename__ = "type_coin"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    coin = Column(String)
