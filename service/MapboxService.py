import json
import os
from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger
from exception.exceptions import CustomError

load_dotenv()

# TODO: Agregar logger
# TODO: Verificar si se puede ocupar decorador para no ocupar try catch a cada rato.


class MapBoxService:
    BASE_COUNTRY = "Chile"
    coordinates_url = os.getenv('MAPBOX_URL')

    async def get_latitude_longitude(self, address: str):
        async with AsyncClient() as client:
            try:
                full_address = address + " " + self.BASE_COUNTRY
                mapbox_url = self.coordinates_url + "/" + full_address
                logger.info("mapbox_url: {}", mapbox_url)

                response = await client.get(url=mapbox_url)
                logger.info("response: {}", response)
                logger.info("response.text: {}", response.text)

                if response.status_code != status.HTTP_200_OK:
                    logger.error("response: {}", response)
                    logger.error("response.text: {}", response.text)
                    raise CustomError(name="Error de geocodificación",
                                      detail=response.text,  # TODO: Llenar campo
                                      status_code=response.status_code,
                                      cause="Dirección inválida de sucursal")

                data = json.loads(response.text)
                logger.info("data: {}", data)

                if 'data' not in data:
                    logger.error("data: {}", data)
                    raise CustomError(name="Error de geocodificación",
                                      detail="No hay datos geocodificados",  # TODO: Llenar campo
                                      status_code=status.HTTP_400_BAD_REQUEST,
                                      cause="Dirección inválida de sucursal")

                return data["data"]

            except RequestError as error:
                logger.error('error: {}', error)
                logger.error('error.args: {}', error.args)
                raise CustomError(name="Error de geocodificación",
                                  detail=error.args[0],
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  cause="")  # TODO: Llenar campo
