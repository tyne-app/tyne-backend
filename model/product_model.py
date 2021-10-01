from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.config import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,)
    description = Column(String)
    category_id = Column(Integer)
    branch_id = Column(Integer)

    items = relationship("Item", back_populates="owner")
