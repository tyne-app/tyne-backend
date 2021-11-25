from sqlalchemy.orm import Session

from repository.entity.BankEntity import BankEntity


def get_all_banks(db: Session):
    return db \
        .query(BankEntity) \
        .all()


def get_bank_by_id(id_bank: int, db: Session):
    return db \
        .query(BankEntity) \
        .filter(BankEntity.id == id_bank) \
        .first()
