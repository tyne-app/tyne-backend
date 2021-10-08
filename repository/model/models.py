from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP, DECIMAL, Float, Text
from sqlalchemy.orm import relationship

from repository.database.database import Base


class Country(Base):
    __tablename__ = 'country'
    __table_args__ = {"schema": "tyne"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class City(Base):
    __tablename__ = 'city'
    __table_args__ = {"schema": "tyne"}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey('tyne.country.id'))


class State(Base):
    __tablename__ = 'state'
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city_id = Column(Integer, ForeignKey('tyne.city.id'))
    city = relationship("City")


class TypeLegalRepresentative(Base):
    __tablename__ = "type_legal_representative"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    # Back FK
    representative_legal = relationship("LegalRepresentative", back_populates='type_legal_representative')
    # represent = relationship('LegalRepresentative',backref='legal_representative_lookup')


class LegalRepresentative(Base):
    __tablename__ = "legal_representative"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    last_name = Column(String(100))
    identifier = Column(String(100))
    email = Column(String(100))
    phone = Column(String(100))

    # FK
    type_legal_representative_id = Column(Integer, ForeignKey('tyne.type_legal_representative.id'), nullable=True)

    # Back FK
    type_legal_representative = relationship('TypeLegalRepresentative', back_populates='representative_legal')
    legalrepresentative_branch = relationship("Branch", back_populates='legal_representative')

    # type_legal_representative = relationship("TypeLegalRepresentative",back_populates="represent")
    # type_legal_representative = relationship("TypeLegalRepresentative")


class Restaurant(Base):
    __tablename__ = "restaurant"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(100))
    name = Column(String(100))
    created_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)

    # FK
    legal_representative_id = Column(Integer, ForeignKey('tyne.legal_representative.id'))
    legal_representative = relationship("LegalRepresentative")
    state_id = Column(Integer, ForeignKey('tyne.state.id'))
    state = relationship("State")

    # Back FK
    restaurant_branch = relationship("Branch", back_populates='restaurant')


class Bank(Base):
    __tablename__ = "bank"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    # Back FK
    restaurants_banks = relationship("BankRestaurant", back_populates='bank')


class BankRestaurant(Base):
    __tablename__ = "bank_restaurant"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    account_holder = Column(String(100))
    account_number = Column(String(100))
    account_type = Column(String(50))

    # FK
    bank_id = Column(Integer, ForeignKey('tyne.bank.id'))

    # Back FK
    bank = relationship('Bank', back_populates='restaurants_banks')


class Schedule(Base):
    __tablename__ = "schedule"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    opening_hour = Column(TIMESTAMP)
    closing_hour = Column(TIMESTAMP)
    is_monday = Column(Boolean)
    is_tuesday = Column(Boolean)
    is_wednesday = Column(Boolean)
    is_thursday = Column(Boolean)
    is_friday = Column(Boolean)
    is_saturday = Column(Boolean)
    is_sunday = Column(Boolean)

    # Back FK
    # branch_schedule = relationship("Branch", back_populates='schedule')


class Category(Base):
    __tablename__ = "category"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    # Back FK
    product_category = relationship("Product", back_populates='category')

    def __init__(self, id=None, name=""):
        self.id = id
        self.name = name


class Branch(Base):
    __tablename__ = "branch"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    accept_pet = Column(Boolean)
    commercial_activity = Column(String(100))
    description = Column(String(100))
    address = Column(String(100))
    longitud = Column(DECIMAL)
    latitud = Column(DECIMAL)

    # FK
    legal_representative_id = Column(Integer, ForeignKey('tyne.legal_representative.id'))
    restaurant_id = Column(Integer, ForeignKey('tyne.restaurant.id'))
    state_id = Column(Integer, ForeignKey('tyne.state.id'))
    bank_restaurant_id = Column(Integer, ForeignKey('tyne.bank_restaurant.id'))
    # schedule_id = Column(Integer, ForeignKey('tyne.schedule.id'))

    legal_representative = relationship("LegalRepresentative", back_populates='legalrepresentative_branch')
    restaurant = relationship("Restaurant", back_populates='restaurant_branch')
    state = relationship("State", foreign_keys='[Branch.state_id]')
    bank_restaurant = relationship("BankRestaurant", foreign_keys='[Branch.bank_restaurant_id]')

    # Back FK
    # menu_branch = relationship("Menu", back_populates='branch')
    # product_branch = relationship("Product", back_populates='branch')
    # children = relationship("product", lazy='joined')


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    url_image = Column(Text)

    # FK
    category_id = Column(Integer, ForeignKey('tyne.category.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    category = relationship("Category", back_populates='product_category')
    # branch = relationship("Branch", back_populates='product_branch')

    # Back ForeignKeys
    price_product = relationship("Price", back_populates='product_price')

    # FALTAN:
    # reservation_product = relationship("Menu", back_populates='product')

    # branch = relationship("TABLE_NAME", back_populates='Other Back FK')

    def __init__(self, id, name, description, url_image, branch_id):
        self.id = id
        self.name = name
        self.description = description
        self.url_image = url_image
        self.branch_id = branch_id

    def product_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_url": self.url_image,
            "price": self.price_product[0].amount
        }

    def get_category_dict(self):
        return {"id": self.category.id, "name": self.category.name}

    def get_category_name(self):
        return self.category.name

    class Config:
        orm_mode = True


class Price(Base):
    __tablename__ = "price"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float(100))
    commission_tyne = Column(Float(100))
    created_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)
    state = Column(Integer)

    # FK
    product_id = Column(Integer, ForeignKey('tyne.product.id'))

    # Back FK
    product_price = relationship("Product", back_populates='price_product')

    def __init__(self, id=None, amount=0, commission_tyne=0, created_date=None, update_date=datetime.now(), state=1):
        self.id = id
        self.amount = amount
        self.commission_tyne = commission_tyne
        self.created_date = created_date
        self.update_date = update_date
        self.state = state

    class Config:
        orm_mode = True
