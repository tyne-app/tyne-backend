from typing import TypeVar, Generic

T = TypeVar('T')


class GenericDTO:
    data: Generic[T] = None
    error: Generic[T] = None
