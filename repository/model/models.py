from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database import Base


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

