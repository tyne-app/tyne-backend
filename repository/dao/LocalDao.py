from loguru import logger
from datetime import datetime, timezone
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchBankEntity import BranchBankEntity
from repository.entity.BranchScheduleEntity import BranchScheduleEntity
from configuration.database.database import SessionLocal
from repository.entity.UserEntity import UserEntity
from repository.entity.BranchImageEntity import BranchImageEntity


class LocalDAO:

    def register_account(self,
                         user_entity: UserEntity,
                         manager_entity: ManagerEntity,
                         legal_representative_entity: LegalRepresentativeEntity,
                         restaurant_entity: RestaurantEntity,
                         branch_entity: BranchEntity,
                         branch_bank_entity: BranchBankEntity,
                         branch_image_entity: BranchImageEntity,
                         db: SessionLocal):

        logger.info('manager_entity: {}, legal_representative_entity: {},'
                    ' restaurant_entity: {}, branch_entity: {}, branch_bank_entity: {}, branch_image_entity: {}',
                    manager_entity, legal_representative_entity, restaurant_entity, branch_entity, branch_bank_entity,
                    branch_image_entity)

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
            db.flush()

            branch_image_entity.branch_id = branch_entity.id
            db.add(branch_image_entity)
            db.commit()
            return True
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.rollback()
            return error.args[0]

    def get_account_profile(self, branch_id: int, db: SessionLocal):
        try:
            profile = {}

            branch_entity = db.query(BranchEntity.id, BranchEntity.manager_id, BranchEntity.accept_pet,
                                     BranchEntity.description,
                                     BranchEntity.state_id, BranchEntity.street, BranchEntity.street_number,
                                     RestaurantEntity.name, RestaurantEntity.commercial_activity,
                                     RestaurantEntity.phone) \
                .select_from(BranchEntity).join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
                .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
                .join(UserEntity, UserEntity.id == ManagerEntity.id_user) \
                .filter(UserEntity.is_active) \
                .filter(BranchEntity.id == branch_id).first()

            profile['branch'] = branch_entity

            if not branch_entity:
                return None

            manager_entity = db.query(ManagerEntity.id, ManagerEntity.last_name,
                                      ManagerEntity.name, ManagerEntity.phone,
                                      ManagerEntity.id_user,
                                      UserEntity.email).select_from(ManagerEntity).join(
                UserEntity,
                UserEntity.id == ManagerEntity.id_user).filter(
                ManagerEntity.id == branch_entity.manager_id).first()

            if not manager_entity:
                return None

            profile['manager'] = manager_entity

            image_list = db.query(BranchImageEntity.id, BranchImageEntity.url_image) \
                .select_from(BranchImageEntity) \
                .join(BranchEntity, BranchEntity.id == BranchImageEntity.branch_id) \
                .filter(BranchImageEntity.branch_id == branch_entity.id).all()

            profile['image_list'] = image_list

            schedule = db.query(BranchScheduleEntity).filter(
                BranchScheduleEntity.branch_id == branch_id).filter(BranchScheduleEntity.active).all()

            profile['schedule_list'] = schedule

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
                       branch_image_entity: BranchImageEntity,
                       db: SessionLocal):
        logger.info('branch_id: {}, manager_entity: {}, branch_entity: {},'
                    ' branch_bank_entity: {}, branch_image_entity: {}',
                    branch_id, manager_entity, branch_entity, branch_bank_entity, branch_image_entity)
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
            db.flush()

            branch_image_entity.branch_id = branch_entity.id
            db.add(branch_image_entity)
            db.commit()
            return True
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
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
