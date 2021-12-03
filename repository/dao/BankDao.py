from sqlalchemy.orm import Session

from repository.entity.BankEntity import BankEntity


class BankDao:

    def get_banks(self, db: Session) -> list[BankEntity]:
        return db \
            .query(BankEntity.id, BankEntity.name) \
            .filter(BankEntity.active) \
            .all()

    def get_bank_by_id(self, id_bank: int, db: Session) -> BankEntity:
        return db \
            .query(BankEntity.id, BankEntity.name) \
            .filter(BankEntity.id == id_bank) \
            .filter(BankEntity.active) \
            .first()
