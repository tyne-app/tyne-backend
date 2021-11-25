from sqlalchemy.orm import *

from repository.entity.BranchEntity import BranchEntity


def get_branch_by_id(db: Session, branch_id: int):
    return db \
        .query(BranchEntity) \
        .filter(BranchEntity.id == branch_id) \
        .first()
