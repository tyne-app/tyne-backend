from loguru import logger
from datetime import datetime
import pytz
from dto.request.local_request_dto import NewBranch
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchBankEntity import BranchBankEntity
from repository.entity.ScheduleEntity import ScheduleEntity
from repository.entity.BranchScheduleEntity import BranchScheduleEntity
from exception.exceptions import CustomError
from configuration.database.database import SessionLocal, get_data_base
from repository.entity.UserEntity import UserEntity


class LocalDAO:

    def register_account(self,
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
            db.add(manager_entity)
            db.flush()

            db.add(legal_representative_entity)
            db.flush()

            restaurant_entity.legal_representative_id = legal_representative_entity.id
            chile_pytz = pytz.timezone('Chile/Continental')
            chile_datetime = datetime.now(chile_pytz)  # TODO: Arreglar horario chile
            restaurant_entity.created_date = chile_datetime
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

    def get_account_pre_login(self, email: str, db: SessionLocal):
        try:
            manager_entity_id = db.query(ManagerEntity.id).filter(ManagerEntity.email == email).first()
            if not manager_entity_id:
                return None
            branch_entity = db.query(BranchEntity.id, BranchEntity.uid, BranchEntity.accept_pet,
                                     BranchEntity.description, BranchEntity.street, BranchEntity.street_number,
                                     RestaurantEntity.name, RestaurantEntity.commercial_activity) \
                .select_from(BranchEntity) \
                .join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
                .filter(BranchEntity.manager_id == manager_entity_id.id) \
                .filter(BranchEntity.is_active).first()
            if not branch_entity:
                return None

            return branch_entity
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            return error.args[0]

    def get_account_profile(self, email: str, db: SessionLocal):
        # TODO: para el login, yo te mando el email y se devuelves todos los datos del local + del representante
        try:
            profile = {}

            manager_entity = db.query(ManagerEntity).filter(ManagerEntity.email == email).first()
            if not manager_entity:
                return None

            profile['manager'] = manager_entity

            branch_entity = db.query(BranchEntity.id, BranchEntity.accept_pet, BranchEntity.description,
                                     BranchEntity.state_id, BranchEntity.street, BranchEntity.street_number,
                                     RestaurantEntity.name, RestaurantEntity.commercial_activity) \
                .select_from(BranchEntity).join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
                .filter(BranchEntity.manager_id == manager_entity.id).filter(BranchEntity.is_active).first()

            profile['branch'] = branch_entity

            if not branch_entity:
                return None

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
                       branch_id: int,
                       manager_entity: ManagerEntity,
                       branch_entity: BranchEntity,
                       branch_bank_entity: BranchBankEntity,
                       db: SessionLocal):
        logger.info('branch_id: {}, manager_entity: {}, branch_entity: {}, branch_bank_entity: {}',
                    branch_id, manager_entity, branch_entity, branch_bank_entity)
        try:
            db.begin()

            db.add(manager_entity)
            db.flush()

            restaurant_entity_id = db.query(BranchEntity.restaurant_id).select_from(BranchEntity). \
                filter(BranchEntity.id == branch_id).first()

            db.add(branch_bank_entity)
            db.flush()

            branch_entity.restaurant_id = restaurant_entity_id
            branch_entity.manager_id = manager_entity.id
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
