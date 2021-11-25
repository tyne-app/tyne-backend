from configuration.database.database import SessionLocal
from repository.entity.OpinionEntity import OpinionEntity


class OpinionDao:

    @classmethod
    def find_by_branch_id(cls, db: SessionLocal, branch_id: int):
        return db \
            .query(OpinionEntity) \
            .filter(OpinionEntity.branch_id == branch_id) \
            .all()
