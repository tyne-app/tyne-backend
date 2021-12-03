from datetime import datetime, timezone

from sqlalchemy.orm import Session
from starlette import status

from repository.entity.BranchBankEntity import BranchBankEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchImageEntity import BranchImageEntity
from repository.entity.BranchScheduleEntity import BranchScheduleEntity
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.UserEntity import UserEntity
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions


class LocalDAO:
    _throwerExceptions = ThrowerExceptions()

    def register_account(self,
                         user_entity: UserEntity,
                         manager_entity: ManagerEntity,
                         legal_representative_entity: LegalRepresentativeEntity,
                         restaurant_entity: RestaurantEntity,
                         branch_entity: BranchEntity,
                         branch_bank_entity: BranchBankEntity,
                         branch_image_entity: BranchImageEntity,
                         db: Session):
        try:
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
        except Exception as ex:
            db.rollback()
            raise ex

    async def get_account_profile(self, branch_id: int, db: Session):
        profile = {}

        branch_entity = db \
            .query(BranchEntity.id, BranchEntity.manager_id, BranchEntity.accept_pet,
                   BranchEntity.description,
                   BranchEntity.state_id, BranchEntity.street, BranchEntity.street_number,
                   RestaurantEntity.name, RestaurantEntity.commercial_activity,
                   RestaurantEntity.phone) \
            .select_from(BranchEntity).join(RestaurantEntity, RestaurantEntity.id == BranchEntity.restaurant_id) \
            .join(ManagerEntity, ManagerEntity.id == BranchEntity.manager_id) \
            .join(UserEntity, UserEntity.id == ManagerEntity.id_user) \
            .filter(UserEntity.is_active) \
            .filter(BranchEntity.id == branch_id) \
            .first()

        profile['branch'] = branch_entity

        if not branch_entity:
            await self._throwerExceptions.throw_custom_exception(name=Constants.ACCOUNT_PROFILE_GET_ERROR,
                                                                 detail=Constants.BRANCH_NOT_FOUND_ERROR_DETAIL,
                                                                 status_code=status.HTTP_204_NO_CONTENT)

        manager_entity = db \
            .query(ManagerEntity.id, ManagerEntity.last_name,
                   ManagerEntity.name, ManagerEntity.phone,
                   ManagerEntity.id_user,
                   UserEntity.email).select_from(ManagerEntity).join(
            UserEntity,
            UserEntity.id == ManagerEntity.id_user) \
            .filter(
            ManagerEntity.id == branch_entity.manager_id) \
            .first()

        if not manager_entity:
            await self._throwerExceptions.throw_custom_exception(name=Constants.ACCOUNT_PROFILE_GET_ERROR,
                                                                 detail=Constants.MANAGER_NOT_FOUND_ERROR_DETAIL,
                                                                 status_code=status.HTTP_204_NO_CONTENT)

        profile['manager'] = manager_entity

        image_list = db \
            .query(BranchImageEntity.id, BranchImageEntity.url_image) \
            .select_from(BranchImageEntity) \
            .join(BranchEntity, BranchEntity.id == BranchImageEntity.branch_id) \
            .filter(BranchImageEntity.branch_id == branch_entity.id) \
            .all()

        profile['image_list'] = image_list

        schedule = db \
            .query(BranchScheduleEntity) \
            .filter(BranchScheduleEntity.branch_id == branch_id) \
            .filter(BranchScheduleEntity.active) \
            .all()

        profile['schedule_list'] = schedule

        return profile

    def add_new_branch(self,
                       user_entity: UserEntity,
                       branch_id: int,
                       manager_entity: ManagerEntity,
                       branch_entity: BranchEntity,
                       branch_bank_entity: BranchBankEntity,
                       branch_image_entity: BranchImageEntity,
                       db: Session):
        try:
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
        except Exception as ex:
            db.rollback()
            raise ex

    def find_branch_by_email_user_manager(self, email: str, db: Session):
        return db \
            .query(BranchEntity) \
            .select_from(BranchEntity) \
            .join(ManagerEntity, BranchEntity.manager_id == ManagerEntity.id) \
            .join(UserEntity, ManagerEntity.id_user == UserEntity.id) \
            .filter(UserEntity.email == email) \
            .first()
