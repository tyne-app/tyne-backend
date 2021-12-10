from loguru import logger
from sqlalchemy import func, distinct, or_
from sqlalchemy.orm import Session

from dto.request.business_request_dto import SearchParameter
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchImageEntity import BranchImageEntity
from repository.entity.BranchScheduleEntity import BranchScheduleEntity
from repository.entity.ClientEntity import ClientEntity
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.OpinionEntity import OpinionEntity
from repository.entity.ProductEntity import ProductEntity
from repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from repository.entity.ReservationEntity import ReservationEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.StateEntity import StateEntity
from repository.entity.UserEntity import UserEntity


class BranchDao:

    def get_branch_by_id(self, db: Session, branch_id: int) -> BranchEntity:
        return db \
            .query(BranchEntity) \
            .filter(BranchEntity.id == branch_id) \
            .first()

    def search_all_branches(self,
                            search_parameters: SearchParameter,
                            db: Session,
                            client_id: int,
                            limit: int):
        all_branches = None

        if client_id:
            all_branches = db.query(
                distinct(BranchEntity.id),
                BranchEntity.id.label(name='branch_id'),
                StateEntity.name.label(name='state_name'),
                StateEntity.id.label(name='state_id'),
                RestaurantEntity.name.label(name='restaurant_name'),
                RestaurantEntity.description.label('restaurant_description'),
                func.avg(OpinionEntity.qualification).over(partition_by=BranchEntity.id).label(name='rating'),
                func.avg(ProductEntity.amount).over(partition_by=BranchEntity.id).label(name='avg_price'),
                func.min(ProductEntity.amount).over(partition_by=BranchEntity.id).label(name='min_price'),
                func.max(ProductEntity.amount).over(partition_by=BranchEntity.id).label(name='max_price'),
                BranchImageEntity.url_image)

        if not client_id:
            all_branches = db.query(
                distinct(BranchEntity.id),
                BranchEntity.id.label(name='branch_id'),
                StateEntity.name.label(name='state_name'),
                StateEntity.id.label(name='state_id'),
                RestaurantEntity.name.label(name='restaurant_name'),
                RestaurantEntity.description.label('restaurant_description'),

                BranchImageEntity.url_image)

        all_branches = all_branches \
            .select_from(BranchEntity) \
            .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
            .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .join(BranchImageEntity, BranchImageEntity.branch_id == BranchEntity.id) \
            .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
            .join(UserEntity, UserEntity.id == ManagerEntity.id_user)

        if client_id:
            all_branches = all_branches \
                .join(ProductEntity, ProductEntity.branch_id == BranchEntity.id, isouter=True) \
                .join(OpinionEntity, OpinionEntity.branch_id == BranchEntity.id, isouter=True)

        all_branches = all_branches \
            .filter(BranchImageEntity.is_main_image) \
            .filter(UserEntity.is_active)

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
                .filter(or_(ReservationChangeStatusEntity.status_id < 3, ReservationChangeStatusEntity == 4)) \
                .filter(ReservationEntity.reservation_date == date_reservation) \
                .group_by(ReservationEntity.id).cte(name='reservation_data')

            all_branches = all_branches.filter(BranchEntity.id.in_(db.query(reservation_data.c.branch_id) \
                .select_from(reservation_data) \
                .group_by(reservation_data.c.branch_id) \
                .having(
                func.count(reservation_data.c.reservation_id) < 4)))

        if search_parameters['state_id']:
            state_id = search_parameters['state_id']
            all_branches = all_branches.filter(StateEntity.id == state_id)

        if search_parameters['sort_by'] and search_parameters['order_by']:  # TODO: Se implementa después
            pass

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
                .join(OpinionEntity, OpinionEntity.branch_id == BranchEntity.id) \
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
            BranchEntity.id.label(name='branch_id'),
            RestaurantEntity.name.label(name='restaurant_name'),
            StateEntity.name.label(name='state_name'),
            BranchEntity.street,
            BranchEntity.street_number,
            BranchEntity.latitude,
            BranchEntity.longitude, ) \
            .select_from(BranchEntity) \
            .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
            .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
            .join(UserEntity, UserEntity.id == ManagerEntity.id_user) \
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

        # opinions = db \
        #     .query(OpinionEntity.id,
        #            OpinionEntity.description,
        #            OpinionEntity.qualification,
        #            OpinionEntity.creation_date,
        #            ClientEntity.name.label(name='client_name')) \
        #     .select_from(OpinionEntity) \
        #     .join(ClientEntity, ClientEntity.id == OpinionEntity.client_id) \
        #     .join(BranchEntity, BranchEntity.id == OpinionEntity.branch_id) \
        #     .filter(BranchEntity.id == branch.id).all()

        # branch_dict['opinions'] = opinions
        return branch_dict
