from pydantic import BaseModel
from typing import Optional


class SearchParameters(BaseModel):
    name: Optional[str]
    date_reservation: Optional[str]
    state_id: Optional[int]
    sort_by: Optional[int]
    order_by: Optional[int]


class PreviewBranch(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None  # TODO: Definir si es oopcional
    price: Optional[int] = 0  # TODO: Descartar Optional, por ahora se deja por poca e inconsistente data
    rating: Optional[float] = 0
    description: Optional[str] = None  # TODO: Creo que es opcional, por confirmar


class PreviewBranchOutput(BaseModel):
    data: Optional[list[PreviewBranch]] = []
    error: Optional[str] = []


class PreviewBranchClient(BaseModel):
    id: int
    name: str
    is_favourite: Optional[bool]
    image_url: Optional[str] = None  # TODO: Definir si es oopcional
    price: Optional[int] = 0  # TODO: Descartar Optional, por ahora se deja por poca e inconsistente data
    rating: Optional[int] = 0
    description: Optional[str] = None  # TODO: Creo que es opcional, por confirmar


class PreviewBranchOutputClient(BaseModel):
    data: Optional[list[PreviewBranchClient]] = []
    error: Optional[str] = []


class BranchProfileView(BaseModel):
    id: int
    name: str
    description: str
    latitude: float
    longitude: float
    accept_pet: bool
    address: Optional[str]
    rating: Optional[float]
    price: Optional[int]
    related_branch: list[dict]
    branch_images: list[dict]
    opinion_list: list[dict]
    schedule_list: Optional[list]


class BranchProfileOutput(BaseModel):
    data: Optional[BranchProfileView] = []
    error: Optional[str] = []
