from sqlalchemy.orm import Session
from src.repository.entity.OpinionEntity import OpinionEntity


class OpinionDao:

    def find_by_branch_id(self, db: Session, branch_id: int):
        return db \
            .query(OpinionEntity) \
            .filter(OpinionEntity.branch_id == branch_id) \
            .all()
