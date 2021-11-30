from sqlalchemy.orm import Session
from starlette import status
from exception.exceptions import CustomError
from repository.entity.PaymentEntity import PaymentEntity
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity


class PaymentDao:

    @classmethod
    def create_payment(cls, payment: PaymentEntity, reservation_status: ReservationChangeStatusEntity,
                       db: Session):
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

    @classmethod
    def get_payment(cls, reservation_id: int, db: Session):
        try:
            return db.query(PaymentEntity).filter(PaymentEntity.reservation_id == reservation_id).first()

        except Exception:
            raise CustomError(name="Error al obtener el pago",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="Error al obtener el pago")
