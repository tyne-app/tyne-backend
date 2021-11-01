from typing import Optional
from pydantic import BaseModel
from datetime import datetime, time

class PreviewBranch(BaseModel):
    branch_id: int
    state_name: str
    state_id: int
    restaurant_name: str
    description: Optional[str] = None
    rating: Optional[float] = 0
    avg_price: Optional[int] = 0
    min_price: Optional[int] = 0
    max_price: Optional[int] = 0
    url_image: str

    class Config:
        orm_mode = True


class ListBranchOutput(BaseModel):
    data: Optional[list[PreviewBranch]] = None
    error: Optional[str] = None


class Branches(BaseModel):
    branch_id: int
    restaurant_name: str
    state_name: str


class Schedule(BaseModel):
    id: int
    day: int
    opening_hour: time
    closing_hour: time

    class Config:
        orm_mode = True


class BranchImages(BaseModel):
    id: int
    url_image: str


class Opinions(BaseModel):
    id: int
    description: str
    qualification: float
    creation_date: datetime
    client_name: str


class BranchProfileView(BaseModel):
    id: int
    description: Optional[str] = None
    latitude: float
    longitude: float
    street: str
    street_number: int
    accept_pet: bool
    name: str

    rating: Optional[float] = None
    avg_price: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    state_name: str

    branches: Optional[list[Branches]] = None
    schedule: Optional[list[Schedule]] = None
    images: Optional[list[BranchImages]] = None
    opinions: Optional[list[Opinions]] = None


class BranchProfileOutput(BaseModel):
    data: Optional[BranchProfileView] = None
    error: Optional[str] = None
