import cloudinary
import cloudinary.api
import cloudinary.uploader
from fastapi import UploadFile
from starlette import status

from src.configuration.Settings import Settings
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions


class CloudinaryService:
    _settings_ = Settings()
    _throwerExceptions = ThrowerExceptions()

    cloudinary.config(
        cloud_name=_settings_.CLOUDINARY_CLOUD_NAME,
        api_key=_settings_.CLOUDINARY_API_KEY,
        api_secret=_settings_.CLOUDINARY_API_SECRET,
        secure=True
    )

    async def upload_image(self, file: UploadFile, user_id: int):
        try:
            folder = self._settings_.ENVIRONMENT + "/users/" + str(user_id)
            response = cloudinary.uploader.upload_image(file, transformation=[{'width':400, 'height':400, 'gravity':"face", 'crop':"fill"}], folder=folder)
            return response
        except cloudinary.exceptions.Error as exception:
            await self._throwerExceptions.throw_custom_exception(name=Constants.IMAGE_UPLOAD_ERROR,
                                                                 detail=Constants.IMAGE_UPLOAD_ERROR,
                                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                 cause=exception)

    async def delete_file(self, id_image: str):
        try:
            response = cloudinary.uploader.destroy(id_image)

            if response["result"] != 'ok':
                await self._throwerExceptions.throw_custom_exception(name=Constants.IMAGE_DELETE_ERROR,
                                                                     detail=Constants.IMAGE_NOT_FOUND_ERROR,
                                                                     status_code=status.HTTP_400_BAD_REQUEST,
                                                                     cause=f"imagen_id {id_image} no encontrada")

            return True
        except cloudinary.exceptions.Error as exception:
            await self._throwerExceptions.throw_custom_exception(name=Constants.IMAGE_DELETE_ERROR,
                                                                 detail=Constants.IMAGE_DELETE_ERROR,
                                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                 cause=exception)
