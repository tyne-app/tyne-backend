from typing import Optional, Union
from pydantic import BaseModel


class MenuOutput(BaseModel):
    data: Optional[list] = []
    error: Optional[str] = []
