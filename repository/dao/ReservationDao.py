from loguru import logger
from sqlalchemy.orm import Session
from starlette import status
from exception.exceptions import CustomError
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from repository.entity.ReservationEntity import ReservationEntity
from repository.entity.ReservationProductEntity import ReservationProductEntity
from repository.entity.ReservationStatusEntity import ReservationStatusEntity


class ReservationDao:

    @classmethod
    def create_reservation(cls, reservation: ReservationEntity, reservation_status: ReservationChangeStatusEntity,
                           products: list[ReservationProductEntity],
                           db: Session):
        try:
            db.add(reservation)
            db.flush()

            reservation_status.reservation_id = reservation.id

            db.add(reservation_status)
            db.flush()

            for x in products:
                x.reservation_id = reservation.id

            db.bulk_save_objects(products)
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
    def update_payment_id_reservation(cls, reservation_id: int, payment_id: str, db: Session):
        try:

            reservation: ReservationEntity = db.query(ReservationEntity) \
                .filter(ReservationEntity.id == reservation_id) \
                .first()

            print(reservation.id)
            if reservation:
                reservation.payment_id = payment_id
                db.commit()
                return reservation

            return reservation
        except Exception as error:
            db.rollback()
            raise CustomError(name="Error al actualizar payment_id reserva",
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

    @classmethod
    def get_reservations(cls, client_id, db: Session):
        try:
            return db.query(ReservationEntity).filter(ReservationEntity.client_id == client_id). \
                join(ReservationEntity.reservation_change_status). \
                join(ReservationChangeStatusEntity.reservation_status).filter(ReservationStatusEntity.id == 4). \
                all()

        except Exception as e:
            logger.error(e)
            raise CustomError(name="Error al guardar estado reserva",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="Error al guardar estado reserva")
