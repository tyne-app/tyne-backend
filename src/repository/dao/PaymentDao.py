from sqlalchemy.orm import Session
from starlette import status
from src.exception.exceptions import CustomError
from src.repository.entity.PaymentEntity import PaymentEntity
from src.repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity


class PaymentDao:

    def create_payment(self, payment: PaymentEntity, reservation_status: ReservationChangeStatusEntity,
                       db: Session) -> PaymentEntity:
        try:
            db.add(payment)
            db.flush()

            db.add(reservation_status)
            db.flush()

            db.commit()

            return payment
        except Exception as error:
            db.rollback()
            raise CustomError(name="Error al guardar pago",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error)

    def get_payment(self, reservation_id: int, db: Session):
        try:
            return db.query(PaymentEntity).filter(PaymentEntity.reservation_id == reservation_id).first()

        except Exception:
            raise CustomError(name="Error al obtener el pago",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="Error al obtener el pago")
