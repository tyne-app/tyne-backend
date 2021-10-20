from fastapi import status
from fastapi.params import Depends
from loguru import logger
from datetime import datetime, timezone
from repository.entity.ManagerEntity import ManagerEntity
from repository.entity.LegalRepresentativeEntity import LegalRepresentativeEntity
from repository.entity.RestaurantEntity import RestaurantEntity
from repository.entity.BranchEntity import BranchEntity
from repository.entity.BranchBankEntity import BranchBankEntity
from exception.exceptions import CustomError
from configuration.database.database import SessionLocal, get_data_base


class LocalDAO:

    def get_database_connection(self):
        # TODO: Retorna conexión a DB
        pass

    def register_account(self,
                         manager_entity: ManagerEntity,
                         legal_representative_entity: LegalRepresentativeEntity,
                         restaurant_entity: RestaurantEntity,
                         branch_entity: BranchEntity,
                         branch_bank_entity: BranchBankEntity,
                         db: SessionLocal):

        logger.info('New manager_entity: {}, legal_representative_entity: {},'
                    ' restaurant_entity: {}, branch_entity: {}, branch_bank_entity: {}',
                    manager_entity, legal_representative_entity, restaurant_entity, branch_entity, branch_bank_entity)

        try:
            db.begin()
            db.add(manager_entity)
            db.flush()

            db.add(legal_representative_entity)
            db.flush()

            restaurant_entity.legal_representative_id = legal_representative_entity.id
            restaurant_entity.created_date = datetime.now()  # TODO: Ajustar datetime a Chile.
            db.add(restaurant_entity)
            db.flush()

            db.add(branch_bank_entity)
            db.flush()

            branch_entity.restaurant_id = restaurant_entity.id
            branch_entity.branch_bank_id = branch_bank_entity.id
            branch_entity.manager_id = manager_entity.id
            db.add(branch_entity)
            db.flush()
            db.commit()
            return True
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.rollback()
            return error.args[0]

    '''
    def get_account_pre_login(email: str, db: Session):
        try:
            legal_representative = db.query(LegalRepresentative.id).filter(LegalRepresentative.email == email).first()
            if not legal_representative:
                return []
            branch = db.query(Branch.id, Branch.uid, Branch.accept_pet, Branch.description, Branch.street,
                              Branch.street_number, Restaurant.name, Restaurant.commercial_activity) \
                .select_from(Branch).join(Restaurant, Restaurant.id == Branch.restaurant_id) \
                .filter(Branch.legal_representative_id == legal_representative.id).first()
            if not branch:
                return []
            return branch
        except Exception as error:
            db.close()
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            return error.args[0]

    def get_account(email: str, db: Session):
        # TODO: para el login, yo te mando el email y se devuelves todos los datos del local + del representante
        try:
            branch_profile = {}
            legal_representative = db.query(LegalRepresentative.id, LegalRepresentative.name,
                                            LegalRepresentative.last_name,
                                            LegalRepresentative.email, LegalRepresentative.phone).select_from(
                LegalRepresentative) \
                .filter(LegalRepresentative.email == email).first()
            branch_profile['legal_representative'] = legal_representative
            if not legal_representative:
                return []

            branch = db.query(Branch.id, Branch.accept_pet, Branch.description, Branch.street, Branch.street_number,
                              Restaurant.name,
                              Restaurant.commercial_activity, State.name.label('state')).select_from(Branch) \
                .join(Restaurant, Restaurant.id == Branch.restaurant_id).join(State, State.id == Branch.state_id) \
                .filter(Branch.legal_representative_id == legal_representative.id).first()
            branch_profile['branch'] = branch

            if not branch:
                return []

            schedule_list = db.query(Schedule).join(BranchSchedule, BranchSchedule.schedule_id == Schedule.id) \
                .join(Branch, Branch.id == BranchSchedule.branch_id) \
                .filter(Branch.legal_representative_id == legal_representative.id).all()
            branch_profile['schedule_list'] = schedule_list

            db.close()
            return branch_profile
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.close()
            return error.args[0]

    def add_branch(new_branch: AddBranch, db: Session):
        logger.info('new_branch: {}', dict(new_branch))
        try:
            db.begin()

            restaurant_id = db.query(Branch.restaurant_id).select_from(Branch).filter(
                Branch.id == new_branch.branch_id).first()

            legal_representative = LegalRepresentative(**new_branch.legal_representative.dict())
            db.add(legal_representative)
            db.flush()

            bank_restaurant = BankRestaurant(**new_branch.bank_restaurant.dict())
            db.add(bank_restaurant)
            db.flush()

            branch = Branch(**new_branch.new_branch.dict())
            branch.legal_representative_id = legal_representative.id
            branch.restaurant_id = restaurant_id["restaurant_id"]
            branch.bank_restaurant_id = bank_restaurant.id
            branch.state = True
            db.add(branch)
            db.flush()
            db.commit()
            branch_id = branch.id
            db.close()
            return branch_id
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            db.close()
            return error.args[0]

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