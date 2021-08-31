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
    is_favourite: Optional[bool]
    image_url: Optional[str] = None  # TODO: Definir si es oopcional
    amount_avg: Optional[int] = 0  # TODO: Descartar Optional, por ahora se deja por poca e inconsistente data
    qualification_avg: Optional[int] = 0
    description: Optional[str] = None  # TODO: Creo que es opcional, por confirmar


class PreviewBranchOutput(BaseModel):
    data: Optional[list[PreviewBranch]] = []
    error: Optional[str] = []