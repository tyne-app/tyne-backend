from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, distinct, extract, subquery
from starlette import status
from exception.exceptions import CustomError
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from repository.entity.ReservationStatusEntity import ReservationStatusEntity
from repository.entity.ReservationEntity import ReservationEntity
from repository.entity.ReservationProductEntity import ReservationProductEntity
from repository.entity.ProductEntity import ProductEntity
from repository.entity.CategoryEntity import CategoryEntity
from repository.entity.ClientEntity import ClientEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.StateEntity import StateEntity
from repository.entity.CityEntity import CityEntity
from repository.entity.CountryEntity import CountryEntity
from datetime import date


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
        reservation: ReservationEntity = db.query(ReservationEntity) \
            .filter(ReservationEntity.id == reservation_id) \
            .first()

        if reservation:
            reservation.payment_id = payment_id
            db.commit()
            return reservation

        return reservation

    @classmethod
    def add_reservation_status(cls, reservation_status: ReservationChangeStatusEntity, db: Session):
        db.add(reservation_status)
        db.commit()
        return reservation_status

    @classmethod
    def local_reservations(cls, db: Session, branch_id: int, reservation_date: date, status_reservation: int):

        if status_reservation == 0:
            filter_status_reservation = [4, 7, 8, 9]
        else:
            filter_status_reservation = [status_reservation]

        sub_query = db.query(ReservationChangeStatusEntity.reservation_id, ReservationChangeStatusEntity.id) \
            .order_by(ReservationChangeStatusEntity.reservation_id.desc(),
                      ReservationChangeStatusEntity.datetime.desc()) \
            .distinct(ReservationChangeStatusEntity.reservation_id) \
            .subquery()

        reservations = db.query(ReservationEntity.id, ReservationEntity.client_id, ClientEntity.name,
                                ClientEntity.last_name,
                                ReservationEntity.preference,
                                ReservationEntity.reservation_date,
                                ReservationEntity.hour,
                                ReservationEntity.people,
                                ReservationChangeStatusEntity.status_id,
                                ReservationStatusEntity.description.label("status_description"),
                                ReservationChangeStatusEntity.datetime.label("reservation_date_status"),
                                BranchEntity.street,
                                BranchEntity.street_number,
                                StateEntity.name.label("state"),
                                CityEntity.name.label("city"),
                                CountryEntity.name.label("country")) \
            .order_by(ReservationEntity.reservation_date.asc(), ReservationEntity.id.desc(),
                      ReservationChangeStatusEntity.datetime.desc()) \
            .filter(ReservationEntity.branch_id == branch_id,
                    ReservationChangeStatusEntity.status_id.in_(filter_status_reservation),
                    extract("month", ReservationEntity.reservation_date) == reservation_date.month,
                    extract("year", ReservationEntity.reservation_date) == reservation_date.year) \
            .join(ClientEntity, ClientEntity.id == ReservationEntity.client_id) \
            .join(ReservationChangeStatusEntity, ReservationChangeStatusEntity.reservation_id == ReservationEntity.id) \
            .join(sub_query, sub_query.c.id == ReservationChangeStatusEntity.id) \
            .join(ReservationStatusEntity, ReservationStatusEntity.id == ReservationChangeStatusEntity.status_id) \
            .join(BranchEntity, BranchEntity.id == ReservationEntity.branch_id) \
            .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
            .join(CityEntity, CityEntity.id == StateEntity.city_id) \
            .join(CountryEntity, CountryEntity.id == CityEntity.country_id) \
            .all()

        return reservations

    @classmethod
    def local_reservations_date(cls, db: Session, branch_id: int, status_reservation: int, reservation_date: date,
                                result_for_page: int,
                                page_number: int):
        if status_reservation == 0:
            filter_status_reservation = [4, 7, 8, 9]
        else:
            filter_status_reservation = [status_reservation]

        sub_query = db.query(ReservationChangeStatusEntity.reservation_id, ReservationChangeStatusEntity.id) \
            .order_by(ReservationChangeStatusEntity.reservation_id.desc(),
                      ReservationChangeStatusEntity.datetime.desc()) \
            .distinct(ReservationChangeStatusEntity.reservation_id) \
            .subquery()

        total_items = db.query(func.count(distinct(ReservationEntity.reservation_date))) \
            .filter(ReservationEntity.branch_id == branch_id,
                    extract("month", ReservationEntity.reservation_date) == reservation_date.month,
                    extract("year", ReservationEntity.reservation_date) == reservation_date.year,
                    ReservationChangeStatusEntity.status_id.in_(filter_status_reservation)) \
            .join(ReservationChangeStatusEntity, ReservationChangeStatusEntity.reservation_id == ReservationEntity.id) \
            .join(sub_query, sub_query.c.id == ReservationChangeStatusEntity.id) \
            .label("total_items")

        reservations_date_response = db \
            .query(ReservationEntity.reservation_date, total_items) \
            .order_by(ReservationEntity.reservation_date.asc()) \
            .filter(ReservationEntity.branch_id == branch_id,
                    extract("month", ReservationEntity.reservation_date) == reservation_date.month,
                    extract("year", ReservationEntity.reservation_date) == reservation_date.year) \
            .join(ReservationChangeStatusEntity, ReservationChangeStatusEntity.reservation_id == ReservationEntity.id) \
            .join(sub_query, sub_query.c.id == ReservationChangeStatusEntity.id)

        reservations_date_response = reservations_date_response.group_by(ReservationEntity.reservation_date)

        total_items_aux = db.query(total_items).first()
        if result_for_page == total_items_aux[0] and page_number == 1:
            result_for_page = result_for_page + 1

        reservations_date_response = reservations_date_response \
            .slice((page_number - 1) * result_for_page, ((page_number - 1) * result_for_page) + result_for_page) \
            .all()

        return reservations_date

    @classmethod
    def reservation_detail(cls, db: Session, reservation_id: int):

        reservation_detail = db.query(ReservationProductEntity.reservation_id,
                                      ClientEntity.name,
                                      ClientEntity.last_name,
                                      ReservationEntity.people,
                                      BranchEntity.street,
                                      BranchEntity.street_number,
                                      StateEntity.name.label("state"),
                                      CityEntity.name.label("city"),
                                      CountryEntity.name.label("country"),
                                      ReservationEntity.preference,
                                      ReservationEntity.reservation_date,
                                      ReservationEntity.hour,
                                      CategoryEntity.id.label("category_id"),
                                      ReservationProductEntity.name_product,
                                      ReservationProductEntity.description.label("product_description"),
                                      ReservationProductEntity.amount.label("product_amount"),
                                      ReservationProductEntity.quantity.label("product_quantity")) \
            .filter(ReservationProductEntity.reservation_id == reservation_id) \
            .join(CategoryEntity, CategoryEntity.name == ReservationProductEntity.category_product) \
            .join(ReservationEntity, ReservationEntity.id == ReservationProductEntity.reservation_id) \
            .join(ClientEntity, ClientEntity.id == ReservationEntity.client_id) \
            .join(BranchEntity, BranchEntity.id == ReservationEntity.branch_id) \
            .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
            .join(CityEntity, CityEntity.id == StateEntity.city_id) \
            .join(CountryEntity, CountryEntity.id == CityEntity.country_id) \
            .all()

        return reservation_detail

    @classmethod
    def get_reservations(cls, client_id, db: Session):
        return db \
            .query(ReservationEntity).filter(ReservationEntity.client_id == client_id) \
            .join(ReservationEntity.reservation_change_status) \
            .join(ReservationChangeStatusEntity.reservation_status).filter(ReservationStatusEntity.id == 4) \
            .all()

    @classmethod
    def get_reservation(cls, reservation_id: int, payment_id: str, db: Session):
        return db.query(ReservationEntity).filter(ReservationEntity.id == reservation_id) \
            .filter(ReservationEntity.payment_id == payment_id) \
            .first()
