import json
import os

from dotenv import load_dotenv
from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger

load_dotenv()


class MapBoxService:

    def __init__(self):
        self.coordinates_url = os.getenv('MAPBOX_URL')

    async def get_latitude_longitude(self, address: str):
        async with AsyncClient() as client:
            try:
                mapbox_url = self.coordinates_url + "/" + address
                logger.info("mapbox_url: {}", mapbox_url)

                response = await client.get(url=mapbox_url)
                logger.info("response: {}", response)
                logger.info("response.text: {}", response.text)

                if response.status_code != status.HTTP_200_OK:
                    logger.error("response: {}", response)
                    logger.error("response.text: {}", response.text)
                    return None
                data = json.loads(response.text)
                logger.info("data: {}", data)

                if 'data' not in data:
                    return None

                return data["data"]
            except RequestError as exc:
                # TODO: Agregar logger
                print(exc)
                print(exc.args)
                return None