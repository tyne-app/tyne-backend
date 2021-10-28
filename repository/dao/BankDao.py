from sqlalchemy.orm import Session
from repository.entity.BankEntity import BankEntity


def get_all_banks(db: Session):
    try:
        banks = db.query(BankEntity).all()
        return banks
    except Exception as error:
        return error.args[0]
    finally:
        db.close()


def get_bank_by_id(id_bank: int, db: Session):
    try:
        bank = db.query(BankEntity).filter(BankEntity.id == id_bank).first()
        return bank
    except Exception as error:
        return error.args[0]
    finally:
        db.close()
