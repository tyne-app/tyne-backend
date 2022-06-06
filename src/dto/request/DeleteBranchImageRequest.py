from pydantic import BaseModel
from starlette import status

from src.exception.exceptions import CustomError


class DeleteBranchImageRequest(BaseModel):
    urlImage: str

    def validate_fields(self):
        if not self.urlImage:
            raise CustomError(name="Url image es inválido",
                              detail="Url image es inválido",
                              status_code=status.HTTP_400_BAD_REQUEST)
