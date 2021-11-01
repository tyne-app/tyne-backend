from loguru import logger
from datetime import datetime, timezone
import pytz
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchBankEntity import BranchBankEntity
from repository.entity.ScheduleEntity import ScheduleEntity
from repository.entity.BranchScheduleEntity import BranchScheduleEntity
from configuration.database.database import SessionLocal
from repository.entity.UserEntity import UserEntity


class LocalDAO:

    def register_account(self,
                         user_entity: UserEntity,
                         manager_entity: ManagerEntity,
                         legal_representative_entity: LegalRepresentativeEntity,
                         restaurant_entity: RestaurantEntity,
                         branch_entity: BranchEntity,
                         branch_bank_entity: BranchBankEntity,
                         db: SessionLocal):

        logger.info('manager_entity: {}, legal_representative_entity: {},'
                    ' restaurant_entity: {}, branch_entity: {}, branch_bank_entity: {}',
                    manager_entity, legal_representative_entity, restaurant_entity, branch_entity, branch_bank_entity)

        try:
            db.begin()

            user_entity.created_date = datetime.now(tz=timezone.utc)
            db.add(user_entity)
            db.flush()

            manager_entity.id_user = user_entity.id
            db.add(manager_entity)
            db.flush()

            db.add(legal_representative_entity)
            db.flush()

            restaurant_entity.legal_representative_id = legal_representative_entity.id
            restaurant_entity.created_date = datetime.now(tz=timezone.utc)
            db.add(restaurant_entity)
            db.flush()

            db.add(branch_bank_entity)
            db.flush()

            branch_entity.restaurant_id = restaurant_entity.id
            branch_entity.branch_bank_id = branch_bank_entity.id
            branch_entity.manager_id = manager_entity.id
            db.add(branch_entity)
            db.commit()
            return True
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.rollback()
            return error.args[0]

    def get_account_profile(self, branch_id: int, db: SessionLocal):
        # TODO: para el login, yo te mando el email y se devuelves todos los datos del local + del representante
        try:
            profile = {}

            branch_entity = db.query(BranchEntity.id, BranchEntity.manager_id, BranchEntity.accept_pet, BranchEntity.description,
                                     BranchEntity.state_id, BranchEntity.street, BranchEntity.street_number,
                                     RestaurantEntity.name, RestaurantEntity.commercial_activity) \
                .select_from(BranchEntity).join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
                .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id)\
                .join(UserEntity, UserEntity.id == ManagerEntity.id_user) \
                .filter(UserEntity.is_active)\
                .filter(BranchEntity.id == branch_id).first()

            profile['branch'] = branch_entity

            if not branch_entity:
                return None

            manager_entity = db.query(ManagerEntity).filter(ManagerEntity.id == branch_entity.manager_id).first()
            if not manager_entity:
                return None

            profile['manager'] = manager_entity

            schedule_entity_list = db.query(ScheduleEntity).join(BranchScheduleEntity,
                                                                 BranchScheduleEntity.schedule_id == ScheduleEntity.id) \
                .join(BranchEntity, BranchEntity.id == BranchScheduleEntity.branch_id) \
                .filter(BranchEntity.manager_id == manager_entity.id).all()

            profile['schedule_list'] = schedule_entity_list

            return profile
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.close()

            return error.args[0]

    def add_new_branch(self,
                       user_entity: UserEntity,
                       branch_id: int,
                       manager_entity: ManagerEntity,
                       branch_entity: BranchEntity,
                       branch_bank_entity: BranchBankEntity,
                       db: SessionLocal):
        logger.info('branch_id: {}, manager_entity: {}, branch_entity: {}, branch_bank_entity: {}',
                    branch_id, manager_entity, branch_entity, branch_bank_entity)
        try:
            db.begin()

            user_entity.created_date = datetime.now(tz=timezone.utc)
            db.add(user_entity)
            db.flush()

            manager_entity.id_user = user_entity.id
            db.add(manager_entity)
            db.flush()

            restaurant_entity_id = db.query(BranchEntity.restaurant_id).select_from(BranchEntity). \
                filter(BranchEntity.id == branch_id).first()
            db.add(branch_bank_entity)
            db.flush()

            branch_entity.restaurant_id = restaurant_entity_id[0]
            branch_entity.manager_id = manager_entity.id
            branch_entity.branch_bank_id = branch_bank_entity.id
            db.add(branch_entity)
            db.commit()
            db.close()
            return True
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.close()
            return error.args[0]

    def find_branch_by_email_user_manager(self, email: str, db: SessionLocal):
        try:
            branch: BranchEntity = db.query(BranchEntity). \
                select_from(BranchEntity). \
                join(ManagerEntity, BranchEntity.manager_id == ManagerEntity.id). \
                join(UserEntity, ManagerEntity.id_user == UserEntity.id). \
                filter(UserEntity.email == email).first()
            return branch
        except Exception as error:
            raise error

    '''
    def update_account(email: str, db: Session, branch_values):
        try:
            # TODO: Saber bien cuales y cómo viene los campos a editar
            branch = db.query(Branch).filter(Branch.id == email).first()
            for key, value in vars(branch_values).items():
                setattr(branch, key, value) if value else None
            branch.update_date = datetime.now()
            db.add(branch)
            branch_id = branch.id
            db.commit()
            return branch_id
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.rollback()
            db.close()
            return error.args[0]

    def delete_account(branch_id: int, db: Session):
        try:
            branch = db.query(Branch).filter(Branch.id == branch_id).first()
            if branch.state is False:
                return branch.id
            branch.state = False
            db.add(branch)
            db.commit()
            branch_id = branch.id
            db.close()
            return branch_id
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.close()
            return error.args[0]
    '''
