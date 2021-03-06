from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.configuration.database.database import Base
from src.repository.entity.CategoryEntity import CategoryEntity

# TODO: Sacar métodos de clase de la entidad
class ProductEntity(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    url_image = Column(Text)
    amount = Column(Integer)

    # FK
    category_id = Column(Integer, ForeignKey('tyne.category.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    branch = relationship('BranchEntity', back_populates="product_branch")
    category: CategoryEntity = relationship('CategoryEntity', back_populates='product')

    def __init__(self, id, category_id, name, description, url_image, amount, branch_id):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.url_image = url_image
        self.branch_id = branch_id
        self.amount = amount

    def product_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_url": self.url_image,
            "amount": self.amount
        }

    def get_category_dict(self):
        return {"id": self.category.id, "name": self.category.name}

    def get_category_name(self):
        return self.category.name

    class Config:
        orm_mode = True
