import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import UploadFile
from starlette import status
from configuration.Settings import Settings
from exception.exceptions import CustomError


class CloudinaryService:
    _settings_ = Settings()

    cloudinary.config(
        cloud_name=_settings_.CLOUDINARY_CLOUD_NAME,
        api_key=_settings_.CLOUDINARY_API_KEY,
        api_secret=_settings_.CLOUDINARY_API_SECRET,
        secure=True
    )

    @classmethod
    def upload_image(cls, file: UploadFile, user_id: int):
        try:
            folder = cls._settings_.ENVIRONMENT + "/users/" + str(user_id)
            response = cloudinary.uploader.upload_image(file, folder=folder)
            return response
        except cloudinary.exceptions.Error as exception:
            raise CustomError(name="Error subir imagen",
                              detail=exception.args[0],
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="")

    @classmethod
    def delete_file(cls, id_image: str):
        try:
            response = cloudinary.uploader.destroy(id_image)

            if response["result"] != 'ok':
                raise CustomError(name="Error eliminar imagen",
                                  detail="Imagen no encontrada",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause="")

            return True
        except cloudinary.exceptions.Error as exception:
            raise CustomError(name="Error eliminar imagen",
                              detail=exception.args[0],
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause="")
