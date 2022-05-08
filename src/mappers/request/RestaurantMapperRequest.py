from loguru import logger
from src.dto.request import Restaurant
from src.repository.entity.RestaurantEntity import RestaurantEntity


class RestaurantMapperRequest:

    def to_restaurant_entity(self, restaurant: Restaurant, name: str):
        logger.info('restaurant: {}', restaurant)
        return RestaurantEntity(**restaurant.dict())
