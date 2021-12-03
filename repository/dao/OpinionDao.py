from sqlalchemy.orm import Session
from repository.entity.OpinionEntity import OpinionEntity


class OpinionDao:

    @classmethod
    def find_by_branch_id(cls, db: Session, branch_id: int):
        return db \
            .query(OpinionEntity) \
            .filter(OpinionEntity.branch_id == branch_id) \
            .all()
