from loguru import logger
from sqlalchemy.orm import Session
from src.repository.entity.ReservationProductEntity import ReservationProductEntity


class ReservationProductDao:

    def get_al_products_by_reservation(self, reservation_id: int, db: Session) -> list:
        products = db.query(ReservationProductEntity.name_product, ReservationProductEntity.quantity)\
            .filter(ReservationProductEntity.reservation_id == reservation_id).all()

        all_products: list = [dict(product) for product in products]

        logger.info("products: {}", products)
        return all_products
