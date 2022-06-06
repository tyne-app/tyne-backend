from loguru import logger
from sqlalchemy import func, distinct, or_
from sqlalchemy.orm import Session
from starlette import status

from src.dto.request.business_request_dto import SearchParameter
from src.exception.exceptions import CustomError
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.BranchImageEntity import BranchImageEntity
from src.repository.entity.BranchScheduleEntity import BranchScheduleEntity
from src.repository.entity.ManagerEntity import ManagerEntity
from src.repository.entity.OpinionEntity import OpinionEntity
from src.repository.entity.ProductEntity import ProductEntity
from src.repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from src.repository.entity.ReservationEntity import ReservationEntity
from src.repository.entity.RestaurantEntity import RestaurantEntity
from src.repository.entity.StateEntity import StateEntity
from src.repository.entity.UserEntity import UserEntity
from src.util.ReservationStatus import ReservationStatus


class BranchDao:

    def get_branch_by_id(self, db: Session, branch_id: int):
        return db \
            .query(BranchEntity.id, RestaurantEntity.name) \
            .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .filter(BranchEntity.id == branch_id) \
            .first()

    def search_all_branches(self,
                            search_parameters: SearchParameter,
                            db: Session,
                            client_id: int,
                            limit: int):

        MAX_RESERVATION_COUNT: int = 4

        all_branches = db.query(
            distinct(BranchEntity.id),
            BranchEntity.id.label(name='branch_id'),
            StateEntity.name.label(name='state_name'),
            StateEntity.id.label(name='state_id'),
            BranchEntity.street.label(name="street"),
            BranchEntity.street_number.label(name="street_number"),
            RestaurantEntity.name.label(name='branch_name'),
            RestaurantEntity.description.label('restaurant_description'),
            func.avg(OpinionEntity.qualification).over(partition_by=BranchEntity.id).label(name='rating'),
            func.avg(ProductEntity.amount).over(partition_by=BranchEntity.id).label(name='avg_price'),
            func.min(ProductEntity.amount).over(partition_by=BranchEntity.id).label(name='min_price'),
            func.max(ProductEntity.amount).over(partition_by=BranchEntity.id).label(name='max_price'),
            BranchImageEntity.url_image)

        all_branches = all_branches \
            .select_from(BranchEntity) \
            .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
            .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .join(BranchImageEntity, BranchImageEntity.branch_id == BranchEntity.id) \
            .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
            .join(UserEntity, UserEntity.id == ManagerEntity.id_user) \
            .join(BranchScheduleEntity, BranchScheduleEntity.branch_id == BranchEntity.id) \
            .join(ProductEntity, ProductEntity.branch_id == BranchEntity.id) \
            .join(OpinionEntity, OpinionEntity.branch_id == BranchEntity.id, isouter=True) \
            .filter(BranchImageEntity.is_main_image) \
            .filter(UserEntity.is_active) \
            .filter(BranchScheduleEntity.active)

        if search_parameters['name']:
            name = search_parameters['name'].lower()
            all_branches = all_branches.filter(func.lower(RestaurantEntity.name).like("%" + name + "%"))

        if search_parameters['date_reservation']:
            date_reservation = search_parameters['date_reservation']
            reservation_data = db.query(
                ReservationEntity.id.label(name='reservation_id'),
                func.max(ReservationChangeStatusEntity.datetime).label(name='last_modify'),
                ReservationEntity.branch_id
            ).select_from(ReservationEntity) \
                .join(ReservationChangeStatusEntity,
                      ReservationChangeStatusEntity.reservation_id == ReservationEntity.id) \
                .filter(ReservationChangeStatusEntity.status_id == ReservationStatus.CONFIRMED) \
                .filter(ReservationEntity.reservation_date == date_reservation) \
                .group_by(ReservationEntity.id).cte(name='reservation_data')

            all_branches = all_branches.filter(BranchEntity.id.not_in(db.query(reservation_data.c.branch_id)
                .select_from(reservation_data)
                .group_by(reservation_data.c.branch_id)
                .having(
                func.count(reservation_data.c.reservation_id) == MAX_RESERVATION_COUNT)))

        if search_parameters['state_id']:
            state_id = search_parameters['state_id']
            all_branches = all_branches.filter(StateEntity.id == state_id)

        if search_parameters['sort_by'] and search_parameters['order_by']:  # TODO: Se implementa después. Refactorizar.
            if search_parameters['order_by'] == 1:
                if search_parameters['sort_by'] == 1:
                    all_branches = all_branches.order_by(
                        (func.avg(OpinionEntity.qualification).over(partition_by=BranchEntity.id)).asc())
                elif search_parameters['sort_by'] == 2:
                    all_branches = all_branches.order_by(RestaurantEntity.name.asc())
                elif search_parameters['sort_by'] == 3:
                    all_branches = all_branches.order_by(
                        (func.max(ProductEntity.amount).over(partition_by=BranchEntity.id)).asc())

            elif search_parameters['order_by'] == 2:
                if search_parameters['sort_by'] == 1:
                    all_branches = all_branches.order_by(
                        (func.avg(OpinionEntity.qualification).over(partition_by=BranchEntity.id)).desc())
                elif search_parameters['sort_by'] == 2:
                    all_branches = all_branches.order_by(RestaurantEntity.name.desc())
                elif search_parameters['sort_by'] == 3:
                    all_branches = all_branches.order_by(
                        (func.min(ProductEntity.amount).over(partition_by=BranchEntity.id)).desc())

        total_number_all_branches = all_branches.count()

        page = search_parameters['page']
        result_for_page = search_parameters['result_for_page']

        if result_for_page == total_number_all_branches and page == 1:
            result_for_page = result_for_page + 1

        all_branches = all_branches \
            .slice((page - 1) * result_for_page, ((page - 1) * result_for_page) + result_for_page)

        all_branches = all_branches.all()

        result_dict = {
            'total_number_all_branches': total_number_all_branches,
            'all_branches': all_branches
        }

        return result_dict

    def search_branch_profile(self, branch_id: int, client_id: int, db: Session):

        branch_dict = {}

        branch = db.query(
            BranchEntity.id,
            BranchEntity.latitude,
            BranchEntity.longitude,
            BranchEntity.street,
            BranchEntity.street_number,
            BranchEntity.accept_pet,
            RestaurantEntity.id.label(name='restaurant_id'),
            RestaurantEntity.name,
            RestaurantEntity.description,
            StateEntity.name.label(name='state_name')) \
            .select_from(BranchEntity) \
            .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
            .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
            .join(UserEntity, UserEntity.id == ManagerEntity.id_user) \
            .filter(BranchEntity.id == branch_id) \
            .filter(UserEntity.is_active).first()

        if not branch:
            return []
        branch_dict['branch'] = branch
        logger.info('branch_dict: {}', branch_dict)

        aggregate_values = None

        if client_id:
            aggregate_values = db.query(
                func.avg(OpinionEntity.qualification).label("rating"),
                func.avg(ProductEntity.amount).label("avg_price"),
                func.max(ProductEntity.amount).label("max_price"),
                func.min(ProductEntity.amount).label("min_price")) \
                .select_from(BranchEntity) \
                .join(OpinionEntity, OpinionEntity.branch_id == BranchEntity.id, isouter=True) \
                .join(ProductEntity, ProductEntity.branch_id == BranchEntity.id) \
                .filter(BranchEntity.id == branch.id).first()

        branch_dict['aggregate_values'] = aggregate_values
        logger.info('branch_dict: {}', branch_dict)

        schedule = db \
            .query(BranchScheduleEntity) \
            .filter(BranchScheduleEntity.branch_id == branch_id) \
            .filter(BranchScheduleEntity.active) \
            .all()

        branch_dict['schedule'] = schedule
        logger.info('branch_dict: {}', branch_dict)

        branches = db.query(
            distinct(BranchEntity.id),
            BranchEntity.id.label(name='branch_id'),
            RestaurantEntity.name.label(name='branch_name'),
            StateEntity.name.label(name='state_name'),
            BranchEntity.street,
            BranchEntity.street_number) \
            .select_from(BranchEntity) \
            .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
            .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
            .join(UserEntity, UserEntity.id == ManagerEntity.id_user) \
            .join(ProductEntity, ProductEntity.branch_id == BranchEntity.id) \
            .join(BranchScheduleEntity, BranchScheduleEntity.branch_id == BranchEntity.id) \
            .filter(RestaurantEntity.id == branch.restaurant_id) \
            .filter(BranchEntity.id != branch.id) \
            .filter(UserEntity.is_active).all()

        branch_dict['branches'] = branches
        logger.info('branch_dict: {}', branch_dict)

        images = db \
            .query(BranchImageEntity.id, BranchImageEntity.url_image) \
            .select_from(BranchImageEntity) \
            .join(BranchEntity, BranchEntity.id == BranchImageEntity.branch_id) \
            .filter(BranchEntity.id == branch.id) \
            .all()

        branch_dict['images'] = images
        logger.info('branch_dict: {}', branch_dict)

        return branch_dict

    def get_day_schedule(self, branch_id: int, day: int, db: Session) -> BranchScheduleEntity:
        return db.query(BranchScheduleEntity) \
            .filter(BranchScheduleEntity.branch_id == branch_id) \
            .filter(BranchScheduleEntity.active) \
            .filter(BranchScheduleEntity.day == day).first()

    def get_name(self, branch_id: int, db: Session) -> str:
        name = db.query(RestaurantEntity.name) \
            .select_from(RestaurantEntity) \
            .join(BranchEntity, BranchEntity.restaurant_id == RestaurantEntity.id) \
            .filter(BranchEntity.id == branch_id) \
            .first()
        logger.info('name: {}', name)
        return name[0]

    def update_schedule(self, schedule: list[BranchScheduleEntity], branch_id: int, db: Session):
        try:
            db.query(BranchScheduleEntity) \
                .filter(BranchScheduleEntity.branch_id == branch_id) \
                .delete()

            db.bulk_save_objects(schedule)
            db.flush()
            db.commit()
        except Exception as error:
            logger.error('Error al guardar horario de la sucursal: {}', error)
            db.rollback()
            raise CustomError(name="Error al guardar el horario de la sucursal",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="Error al guardar el horario de la sucursal")

    def get_images(self, branch_id: int, db: Session):
        return db.query(BranchImageEntity.url_image, BranchImageEntity.id) \
            .filter(BranchImageEntity.branch_id == branch_id) \
            .order_by(BranchImageEntity.id.asc()) \
            .all()

    def add_image(self, branch_id: int, url_image: str, is_main: bool, db: Session):
        try:
            image = BranchImageEntity()
            image.branch_id = branch_id
            image.url_image = url_image
            image.is_main_image = is_main

            db.add(image)
            db.flush()
            db.commit()
            return image
        except Exception as error:
            raise CustomError(name="Error al guardar imagen para branch " + str(branch_id),
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error)

    def delete_image(self, branch_id: int, url_image: str, db: Session):
        try:
            image = db.query(BranchImageEntity).filter(BranchImageEntity.branch_id == branch_id,
                                                       BranchImageEntity.url_image == url_image).first()
            db.delete(image)
            db.flush()
            db.commit()
        except Exception as error:
            raise CustomError(name="Error al eliminar imagen para branch " + str(branch_id),
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error)

    def update_main_image(self, branchImageId: int, db: Session):
        try:
            image: BranchImageEntity = db.query(BranchImageEntity).filter(BranchImageEntity.id == branchImageId).first()
            image.is_main_image = True
            db.flush()
            db.commit()
        except Exception as error:
            raise CustomError(name="Error al actualizar is_main_image",
                              detail="Error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error)
