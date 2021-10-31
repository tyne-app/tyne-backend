from typing import Optional
from pydantic import BaseModel


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
