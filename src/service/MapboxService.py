import json

from fastapi import status
from httpx import AsyncClient, RequestError
from loguru import logger

from src.configuration.Settings import Settings
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions


class MapBoxService:
    BASE_COUNTRY = "Chile"
    KEY_WORD_PLACE = "place"
    KEY_WORD_COUNTRY = "country"
    settings = Settings()
    _throwerExceptions = ThrowerExceptions()

    async def get_latitude_longitude(self, address: str, state_name: str):
        async with AsyncClient() as client:
            try:
                mapbox_api = self.settings.MAPBOX_API
                mapbox_access_token = self.settings.MAPBOX_ACCESS_TOKEN
                full_address = address
                logger.info("mapbox_appi: {}, mapbox_access_token: {}, full_addres: {}", full_address, mapbox_api,
                            mapbox_access_token)

                mapbox_url = mapbox_api + full_address + ".json?types=address&access_token=" + mapbox_access_token
                logger.info("mapbox_url: {}", mapbox_url)

                response = await client.get(url=mapbox_url)
                logger.info("response: {}", response)
                logger.info("response.text: {}", response.text)

                if response.status_code != status.HTTP_200_OK:
                    logger.error("response: {}", response)
                    logger.error("response.text: {}", response.text)
                    await self._throwerExceptions.throw_custom_exception(name=Constants.GEO_DECODE_ERROR,
                                                                         detail=Constants.GEO_DECODE_ERROR,
                                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                         cause=response.text)

                data = json.loads(response.text)
                raw_coordenates = self.extract_coordinates(data=data, state_name=state_name)
                logger.info("raw_coordenates: {}", raw_coordenates)

                if not raw_coordenates:
                    await self._throwerExceptions.throw_custom_exception(name=Constants.GEO_COORDENATES_EMPTY_ERROR,
                                                                         detail=Constants.GEO_COORDENATES_EMPTY_ERROR,
                                                                         status_code=status.HTTP_400_BAD_REQUEST,
                                                                         cause="Dirección inválida de sucursal")
                coordenates = {
                    'latitude': raw_coordenates[1],
                    'longitude': raw_coordenates[0]
                }
                logger.info("coordenates: {}", coordenates)

                return coordenates

            except RequestError as error:
                await self._throwerExceptions.throw_custom_exception(name=Constants.GEO_DECODE_ERROR,
                                                                     detail=Constants.GEO_DECODE_ERROR,
                                                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                     cause=error)

    def extract_coordinates(self, data, state_name: str):
        # logger.info("data: {}", data)

        features = data['features']
        # logger.info("features: {}", features)

        coordenates = None
        is_state = False
        is_country = False

        for feature in features:
            # logger.info("feature: {}", feature)
            contexts = feature['context']
            # logger.info("contexts: {}", contexts)

            for context in contexts:
                # logger.info("context: {}", context)

                if self.KEY_WORD_PLACE.lower() in context['id'].lower():
                    if state_name.lower() in context['text'].lower():
                        is_state = True

                if self.KEY_WORD_COUNTRY.lower() in context['id'].lower():
                    if self.BASE_COUNTRY.lower() in context['text'].lower():
                        is_country = True

                if is_state and is_country:
                    coordenates = feature['center']
                    #logger.info("coordenates: {}", coordenates)
                    return coordenates

        print(state_name)
        print(is_state)
        print(is_country)
        return coordenates
