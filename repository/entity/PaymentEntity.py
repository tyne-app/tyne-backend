from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class PaymentEntity(Base):
    __tablename__ = "payment"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    date = Column(TIMESTAMP)
    method = Column(String)
    amount = Column(Integer)
    receipt_url = Column(String)

    type_coin_id = Column(Integer)
    reservation_id = Column(Integer, ForeignKey("tyne.reservation.id"))
