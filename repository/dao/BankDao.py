from sqlalchemy.orm import Session

from repository.entity.BankEntity import BankEntity


class BankDao:

    def get_banks(self, db: Session):
        return db \
            .query(BankEntity) \
            .all()

    def get_bank_by_id(self, id_bank: int, db: Session):
        return db \
            .query(BankEntity) \
            .filter(BankEntity.id == id_bank) \
            .first()
