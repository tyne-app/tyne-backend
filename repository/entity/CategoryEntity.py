from sqlalchemy import Column, Integer, String, Boolean

from configuration.database.database import Base


class CategoryEntity(Base):
    __tablename__ = "category"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_active = Column(Boolean)
    order = Column(Integer)


    def __init__(self, id=None, name=""):
        self.id = id
        self.name = name

