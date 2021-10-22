from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from configuration.database.database import Base


class PaymentEntity(Base):
    __tablename__ = "payment"
    __table_args__ = {'schema': 'tyne'}

    id = Column(Integer, primary_key=True, index=True)

    payment_date = Column(TIMESTAMP)
    created_date = Column(TIMESTAMP)
    update_date = Column(TIMESTAMP)
    method = Column(String)
    amount = Column(Integer)

    type_coin_id = Column(Integer, ForeignKey("tyne.type_coin.id"))
    reservation_id = Column(Integer, ForeignKey("tyne.reservation.id"))
