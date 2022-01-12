from loguru import logger
from sqlalchemy import func, distinct, or_
from src.configuration.database.database import SessionLocal
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.StateEntity import StateEntity
from src.repository.entity.RestaurantEntity import RestaurantEntity
from src.repository.entity.OpinionEntity import OpinionEntity
from src.repository.entity.ProductEntity import ProductEntity
from src.repository.entity.ReservationEntity import ReservationEntity
from src.repository.entity.ManagerEntity import ManagerEntity
from src.repository.entity.UserEntity import UserEntity
from src.repository.entity.ReservationChangeStatusEntity import ReservationChangeStatusEntity
from src.repository.entity.BranchScheduleEntity import BranchScheduleEntity
from src.repository.entity.BranchImageEntity import BranchImageEntity
from src.repository.entity.ClientEntity import ClientEntity
from src.dto.request.business_request_dto import SearchParameter


class SearchDAO:

    def search_all_branches(self, search_parameters: SearchParameter, db: SessionLocal,
                            client_id: int, limit: int):
        try:

            all_branches = None
            print(client_id)
            if client_id:
                all_branches = db.query(
                    distinct(BranchEntity.id),
                    BranchEntity.id.label(name='branch_id'),
                    StateEntity.name.label(name='state_name'),
                    StateEntity.id.label(name='state_id'),
                    RestaurantEntity.name.label(name='restaurant_name'),
                    BranchEntity.description,
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
                    BranchEntity.description,
                    BranchImageEntity.url_image)

            all_branches = all_branches.select_from(BranchEntity) \
                .join(StateEntity, StateEntity.id == BranchEntity.state_id) \
                .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
                .join(BranchImageEntity, BranchImageEntity.branch_id == BranchEntity.id) \
                .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
                .join(UserEntity, UserEntity.id == ManagerEntity.id_user)

            if client_id:
                all_branches = all_branches.join(ProductEntity, ProductEntity.branch_id == BranchEntity.id,
                                                 isouter=True) \
                    .join(OpinionEntity, OpinionEntity.branch_id == BranchEntity.id, isouter=True)

            all_branches = all_branches.filter(BranchImageEntity.is_main_image) \
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
                if search_parameters['order_by'] == 1:
                    if search_parameters['sort_by'] == 1:
                        all_branches = all_branches.order_by((func.avg(OpinionEntity.qualification).over(partition_by=BranchEntity.id)).asc())
                    elif search_parameters['sort_by'] == 2:
                        all_branches = all_branches.order_by(RestaurantEntity.name.asc())
                    elif search_parameters['sort_by'] == 3:
                        all_branches = all_branches.order_by((func.max(ProductEntity.amount).over(partition_by=BranchEntity.id)).asc())

                elif search_parameters['order_by'] == 2:
                    if search_parameters['sort_by'] == 1:
                        all_branches = all_branches.order_by((func.avg(OpinionEntity.qualification).over(partition_by=BranchEntity.id)).asc())
                    elif search_parameters['sort_by'] == 2:
                        all_branches = all_branches.order_by(BranchEntity.name.desc())
                    elif search_parameters['sort_by'] == 3:
                        all_branches = all_branches.order_by((func.min(ProductEntity.amount).over(partition_by=BranchEntity.id)).desc())

            total_number_all_branches = all_branches.count()

            page = search_parameters['page']
            result_for_page = search_parameters['result_for_page']

            if result_for_page == total_number_all_branches and page == 1:
                result_for_page = result_for_page + 1

            all_branches = all_branches.slice((page - 1) * result_for_page, (
                    (page - 1) * result_for_page) + result_for_page)

            all_branches = all_branches.all()

            result_dict = {
                'total_number_all_branches': total_number_all_branches,
                'all_branches': all_branches
            }

            return result_dict
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            return error.args[0]

    def search_branch_profile(self, branch_id: int, client_id: int, db: SessionLocal):
        try:
            logger.info('branch_id: {}, client_id: {}', branch_id, client_id)

            branch_dict = {}
            logger.info('branch_dict: {}', branch_dict)

            branch = db.query(
                BranchEntity.id,
                BranchEntity.description,
                BranchEntity.latitude,
                BranchEntity.longitude,
                BranchEntity.street,
                BranchEntity.street_number,
                BranchEntity.accept_pet,
                RestaurantEntity.id.label(name='restaurant_id'),
                RestaurantEntity.name,
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

            schedule = db.query(BranchScheduleEntity).filter(
                BranchScheduleEntity.branch_id == branch_id).filter(BranchScheduleEntity.active).all()

            branch_dict['schedule'] = schedule
            logger.info('branch_dict: {}', branch_dict)

            branches = db.query(
                BranchEntity.id.label(name='branch_id'),
                RestaurantEntity.name.label(name='restaurant_name'),
                StateEntity.name.label(name='state_name')) \
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

            images = db.query(BranchImageEntity.id, BranchImageEntity.url_image) \
                .select_from(BranchImageEntity) \
                .join(BranchEntity, BranchEntity.id == BranchImageEntity.branch_id) \
                .filter(BranchEntity.id == branch.id).all()

            branch_dict['images'] = images
            logger.info('branch_dict: {}', branch_dict)

            opinions = db.query(OpinionEntity.id,
                                OpinionEntity.description,
                                OpinionEntity.qualification,
                                OpinionEntity.creation_date,
                                ClientEntity.name.label(name='client_name')) \
                .select_from(OpinionEntity) \
                .join(ClientEntity, ClientEntity.id == OpinionEntity.client_id) \
                .join(BranchEntity, BranchEntity.id == OpinionEntity.branch_id) \
                .filter(BranchEntity.id == branch.id).all()

            branch_dict['opinions'] = opinions
            logger.info('branch_dict: {}', branch_dict)
            return branch_dict

        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            return error.args[0]

    '''
    def read_branch(branch_id: int, db: Session):
        logger.info('branch_id: {}', branch_id)

        try:
            # TODO: Se puede refactorizar los pasos mezclando queries.
            # TODO: Falta caso uso cuando no hay datos para todos o ciertas queries.
            attributes_dict = {}
            # TODO: 1.- Query Branch listo.
            branch = db.query(
                Branch.id, Branch.description, Branch.latitude, Branch.longitude,
                Branch.accept_pet, Branch.street, Branch.street_number, Branch.restaurant_id, Restaurant.name)\
                .select_from(Branch).join(Restaurant, Restaurant.id == Branch.restaurant_id)\
                .filter(Branch.id == branch_id).filter(Branch.state).first()

            if not branch:
                return []

            attributes_dict['branch'] = branch

            # TODO: 2.- Query datos calculados

            aggregate_values = db.query(
                func.avg(Opinion.qualification).label("rating"),
                func.avg(Price.amount).label("price"),
                func.max(Price.amount).label("max_price"),
                func.min(Price.amount).label("min_price")
            ) \
                .select_from(Branch) \
                .join(Opinion, Opinion.branch_id == Branch.id) \
                .join(Product, Product.branch_id == Branch.id) \
                .join(Price, Price.product_id == Product.id) \
                .filter(Branch.id == branch_id) \
                .group_by(Branch.id) \
                .first()
            attributes_dict['aggregate_values'] = aggregate_values

            # TODO: 3.- Query schedule

            schedule_branch = db.query(Schedule).join(BranchSchedule, BranchSchedule.schedule_id == Schedule.id)\
                .join(Branch, Branch.id == BranchSchedule.branch_id).all()
            attributes_dict['schedule_branch'] = schedule_branch
            # TODO: 4.- Query branch del mismo restaurant.

            related_branch = db.query(Branch.id, Restaurant.name) \
                .select_from(Branch).join(Restaurant, Restaurant.id == Branch.restaurant_id)\
                .filter(Branch.restaurant_id == branch.restaurant_id) \
                .filter(Branch.id != branch.id).all()

            attributes_dict['related_branch'] = related_branch
            # TODO: 5.- Query Obtener todas las imagenes del branch. DEVUELVE UNA LISTA.

            branch_images = db.query(Image.id, Image.url) \
                .select_from(BranchImage) \
                .join(Image, Image.id == BranchImage.image_id) \
                .filter(BranchImage.branch_id == branch_id).all()
            attributes_dict['branch_images'] = branch_images
            # TODO: 6.- Query todas las opiniones de forma descendente segun branch.

            opinion_list = db.query(
                Opinion.id, Opinion.description, Opinion.qualification, Opinion.creation_date, Client.name, Client.last_name
            ) \
                .select_from(Opinion) \
                .join(Client, Client.id == Opinion.client_id) \
                .filter(Opinion.branch_id == branch_id) \
                .all()
            attributes_dict['opinion_list'] = opinion_list
            db.close()
            return attributes_dict
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            return error.args[0]
'''
