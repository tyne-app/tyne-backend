from typing import Optional, Union
from pydantic import BaseModel
from dto.dto import GenericDTO as wrapperDTO
from dto.response.search_response import PreviewBranch


class ParserDTO:
    def to_branch_profile(self):
        pass

    def to_branch_profile_response(self):
        pass


class SearchParameter(BaseModel):

    name: Optional[str] = None
    dateReservation: Optional[str] = None
    stateId: Optional[int] = None
    sortBy: Optional[Union[int, str]] = None
    orderBy: Optional[Union[int, str]] = None

    @classmethod
    def to_search_branches_response(cls, content: list[PreviewBranch]):
        response = wrapperDTO()
        response.data = content
        return response.__dict__
