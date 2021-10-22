from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class ReservationProductEntity(Base):
    __tablename__ = "reservation_product"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("tyne.product.id"))
    reservation_id = Column(Integer, ForeignKey("tyne.reservation.id"))
