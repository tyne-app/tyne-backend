from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from repository.model import models
from schema_request import menu_schema


def get_menu(db: Session, branch_id: int):
    # menus: list[models.Menu] = db.query(models.Menu).filter(models.Menu.branch_id == branch_id).all()
    # print(menus[0].id)
    # print(menus[1].id)
    try:
        return db.query(models.Menu).filter(models.Menu.branch_id == branch_id).first()
    except SQLAlchemyError as error:
        print(f'Error: {error}')
        return False
