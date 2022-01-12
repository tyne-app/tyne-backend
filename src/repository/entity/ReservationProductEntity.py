from sqlalchemy import Integer, String, Column, ForeignKey, Float

from src.configuration.database.database import Base


class ReservationProductEntity(Base):
    __tablename__ = "reservation_product"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey('tyne.reservation.id'))
    name_product = Column(String)
    description = Column(String)
    category_product = Column(String)
    amount = Column(Float(100))
    commission_tyne = Column(Float(100))
    quantity = Column(Integer)

