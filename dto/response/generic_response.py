from typing import TypeVar, Generic

T = TypeVar('T')


class GenericResponse:
    data: Generic[T]
    error: Generic[T]

    def __init__(self):
        self.data = [],
        self.error = []


def create_response(data):
    generic = GenericResponse()

    if type(data) != str:
        generic.data = data
    else:
        generic.error = data

    return generic
