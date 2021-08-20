from typing import TypeVar, Generic

T = TypeVar('T')


class GenericDTO:
    data: Generic[T]
    error: Generic[T]