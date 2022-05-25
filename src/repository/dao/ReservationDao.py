from fastapi import status
from loguru import logger
from pytz import timezone
from sqlalchemy import func, distinct, extract
from sqlalchemy.orm import Session
from datetime import date, datetime
from src.exception.exceptions import CustomError
from src.configuration.database.database import _engine
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.BranchImageEntity import BranchImageEntity
from src.repository.entity.CategoryEntity import CategoryEntity
from src.repository.entity.CityEntity import CityEntity
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.CountryEntity import CountryEntity
from src.repository.entity.PaymentEntity import PaymentEntity
from src.repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from src.repository.entity.ReservationEntity import ReservationEntity
from src.repository.entity.ReservationProductEntity import ReservationProductEntity
from src.repository.entity.ReservationStatusEntity import ReservationStatusEntity
from src.repository.entity.RestaurantEntity import RestaurantEntity
from src.repository.entity.StateEntity import StateEntity
from src.util.ReservationStatus import ReservationStatus


class ReservationDao:
    _country_time_zone = timezone('Chile/Continental')

    def create_reservation(self, reservation: ReservationEntity, products: list[ReservationProductEntity],
                           db: Session) -> int:
        try:
            db.add(reservation)
            db.flush()

            for product in products:
                product.reservation_id = reservation.id

            db.bulk_save_objects(products)
            db.commit()
            return reservation.id
        except Exception as ex:
            db.rollback()
            raise ex

    def update_payment_id_reservation(self, reservation_id: int, payment_id: str,
                                      db: Session):  # TODO: Parece que no es necesario
        reservation: ReservationEntity = db \
            .query(ReservationEntity) \
            .filter(ReservationEntity.id == reservation_id) \
            .first()

        if reservation:
            reservation.payment_id = payment_id
            db.commit()
            return reservation

        return reservation

    def add_reservation_status(self, status: int, reservation_id: int):
        reservation_status = ReservationChangeStatusEntity()
        reservation_status.status_id = status
        reservation_status.datetime = datetime.now(self._country_time_zone)
        reservation_status.reservation_id = reservation_id
        logger.info("reservation_status: {}", reservation_status.__dict__)
        '''
           Se ocupa with por temas de threading. Se debe cambiar, la formar de persistir ocupando thread o
           toda la lógica de thread (evento reserva)
        '''
        with Session(_engine) as database_session:
            database_session.add(reservation_status)
            database_session.commit()

    def local_reservations(self, db: Session, branch_id: int, reservation_date: date, status_reservation: int):

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
                                CountryEntity.name.label("country"),
                                ReservationEntity.payment_id) \
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

    def local_reservations_date(self, db: Session, branch_id: int, status_reservation: int, reservation_date: date,
                                result_for_page: int,
                                page_number: int):
        if status_reservation == 0:
            filter_status_reservation = [4, 7, 8, 9]
        else:
            filter_status_reservation = [status_reservation]

        sub_query = db \
            .query(ReservationChangeStatusEntity.reservation_id, ReservationChangeStatusEntity.id) \
            .order_by(ReservationChangeStatusEntity.reservation_id.desc(),
                      ReservationChangeStatusEntity.datetime.desc()) \
            .distinct(ReservationChangeStatusEntity.reservation_id) \
            .subquery()

        total_items = db \
            .query(func.count(distinct(ReservationEntity.reservation_date))) \
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

        return reservations_date_response

    def reservation_detail(self, reservation_id: int, db: Session) -> list:
        # TODO: Agregar Id estado reserva
        reservation_detail: list = db.query(ReservationProductEntity.reservation_id,
                                            ClientEntity.name,
                                            ClientEntity.last_name,
                                            ReservationEntity.people,
                                            ReservationEntity.preference,
                                            BranchEntity.street,
                                            BranchEntity.street_number,
                                            StateEntity.name.label("state"),
                                            CityEntity.name.label("city"),
                                            CountryEntity.name.label("country"),
                                            ReservationEntity.reservation_date,
                                            ReservationEntity.hour,
                                            ReservationEntity.payment_id,
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

    def get_reservations(self, client_id, db: Session):

        return db \
            .query(ReservationEntity.id,
                   RestaurantEntity.name.label("branch_name"),
                   ReservationEntity.people,
                   ReservationEntity.reservation_date,
                   ReservationEntity.hour,
                   PaymentEntity.amount,
                   BranchEntity.street.label("branch_street_address"),
                   BranchEntity.street_number.label("branch_street_number"),
                   BranchImageEntity.url_image,
                   PaymentEntity.date.label("payment_datetime"),
                   ReservationChangeStatusEntity.status_id) \
            .join(BranchEntity, BranchEntity.id == ReservationEntity.branch_id) \
            .join(PaymentEntity, PaymentEntity.reservation_id == ReservationEntity.id) \
            .join(BranchImageEntity, BranchImageEntity.branch_id == BranchEntity.id) \
            .join(ReservationChangeStatusEntity, ReservationChangeStatusEntity.reservation_id == ReservationEntity.id) \
            .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .filter(ReservationEntity.client_id == client_id) \
            .filter(BranchImageEntity.is_main_image) \
            .order_by(ReservationEntity.reservation_date.desc()) \
            .order_by(ReservationChangeStatusEntity.datetime.desc()) \
            .all()

    def get_reservation(self, reservation_id: int, payment_id: str, db: Session) -> ReservationEntity:

        return db \
            .query(ReservationEntity).filter(ReservationEntity.id == reservation_id) \
            .filter(ReservationEntity.payment_id == payment_id) \
            .first()

    def get_reservation_count_by_date(self, branch_id: int, date_reservation: date, db: Session) -> int:
        return db.query(ReservationEntity) \
            .join(ReservationChangeStatusEntity, ReservationChangeStatusEntity.reservation_id == ReservationEntity.id) \
            .filter(ReservationEntity.branch_id == branch_id) \
            .filter(ReservationEntity.reservation_date == date_reservation) \
            .filter(ReservationChangeStatusEntity.status_id == ReservationStatus.CONFIRMED).count()

    def get_last_reservation_status(self, reservation_id: int, db: Session) -> ReservationChangeStatusEntity:

        last_reservation_status = db.query(ReservationChangeStatusEntity.status_id) \
            .select_from(ReservationChangeStatusEntity) \
            .join(ReservationEntity, ReservationEntity.id == ReservationChangeStatusEntity.reservation_id) \
            .filter(ReservationEntity.id == reservation_id) \
            .order_by(ReservationChangeStatusEntity.datetime.desc()).first()

        if not last_reservation_status:
            raise CustomError(name="Error no existe estado de reserva",
                              detail="Estado de reserva no existente para la reserva actual",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Estado de reserva no no existente para la reserva actual")
        return last_reservation_status[0]

    def get_reservation_by_client(self, reservation_id: int, client_id: int, db: Session):
        return db \
            .query(ReservationEntity) \
            .filter(ReservationEntity.id == reservation_id) \
            .filter(ReservationEntity.client_id == client_id) \
            .first()
