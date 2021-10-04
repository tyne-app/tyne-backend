from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP, DECIMAL
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


class Image(Base):
    __tablename__ = "image"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String)
    creation_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)

    # Back FK
    branchimage_image = relationship("BranchImage", back_populates='image')


class BranchImage(Base):
    __tablename__ = "branch_image"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    # FK
    image_id = Column(Integer, ForeignKey('tyne.image.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    # Back FK
    image = relationship("Image", back_populates='branchimage_image')
    branch = relationship("Branch", back_populates='branchimage_branch')


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
    branchimage_branch = relationship("BranchImage", back_populates='branch')
    menu_branch = relationship("Menu", back_populates='branch')
    product_branch = relationship("Product", back_populates='branch')


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, )
    description = Column(String)

    # FK
    category_id = Column(Integer, ForeignKey('tyne.category.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    # Back ForeignKeys
    category = relationship("Category", back_populates='product_category')
    branch = relationship("Branch", back_populates='product_branch')

    menu_product = relationship("Menu", back_populates='product')


class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = {"schema": "tyne"}

    id = Column(Integer, primary_key=True, index=True)

    # ForeignKeys
    product_id = Column(Integer, ForeignKey('tyne.product.id'))
    branch_id = Column(Integer, ForeignKey('tyne.branch.id'))

    # Back FK
    product = relationship("Product", back_populates='menu_product')
    branch = relationship("Branch", back_populates='menu_branch')

    # branch = relationship("TABLE_NAME", back_populates='Other Back FK')
