from sqlalchemy.orm import Session
from starlette import status
from exception.exceptions import CustomError
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from repository.entity.ReservationEntity import ReservationEntity


class ReservationDao:

    @classmethod
    def create_reservation(cls, reservation: ReservationEntity, reservation_status: ReservationChangeStatusEntity,
                           db: Session):
        try:
            db.add(reservation)
            db.flush()

            reservation_status.reservation_id = reservation.id

            db.add(reservation_status)
            db.flush()

            db.commit()

            return reservation
        except Exception as error:
            db.rollback()
            raise CustomError(name="Error al guardar reserva",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error)

    @classmethod
    def add_reservation_status(cls, reservation_status: ReservationChangeStatusEntity, db: Session):
        try:
            db.add(reservation_status)
            db.commit()
            return reservation_status
        except Exception:
            raise CustomError(name="Error al guardar estado reserva",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="Error al guardar estado reserva")
