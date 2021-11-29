import cloudinary
import cloudinary.api
import cloudinary.uploader
from fastapi import UploadFile
from starlette import status

from configuration.Settings import Settings
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions


class CloudinaryService:
    _settings_ = Settings()
    _throwerExceptions = ThrowerExceptions()

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
            await cls._throwerExceptions.throw_custom_exception(name=Constants.IMAGE_UPLOAD_ERROR,
                                                                detail=Constants.IMAGE_UPLOAD_ERROR,
                                                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                cause=exception)

    @classmethod
    def delete_file(cls, id_image: str):
        try:
            response = cloudinary.uploader.destroy(id_image)

            if response["result"] != 'ok':
                await cls._throwerExceptions.throw_custom_exception(name=Constants.IMAGE_DELETE_ERROR,
                                                                    detail=Constants.IMAGE_NOT_FOUND_ERROR,
                                                                    status_code=status.HTTP_400_BAD_REQUEST,
                                                                    cause=f"imagen_id {id_image} no encontrada")

            return True
        except cloudinary.exceptions.Error as exception:
            await cls._throwerExceptions.throw_custom_exception(name=Constants.IMAGE_DELETE_ERROR,
                                                                detail=Constants.IMAGE_DELETE_ERROR,
                                                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                cause=exception)
