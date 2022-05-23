from pydantic import BaseModel


class ScheduleDto(BaseModel):
    opening_hour: str
    closing_hour: str
    active: bool
    day: int


class NewBranchScheduleDto(BaseModel):
    branch_id: int
    schedule: list[ScheduleDto]
