from loguru import logger
from src.dto.request import Restaurant
from src.repository.entity.RestaurantEntity import RestaurantEntity


class RestaurantMapperRequest:

    def to_restaurant_entity(self, restaurant: Restaurant, name: str):
        logger.info('restaurant: {}', restaurant)

        restaurant_entity = RestaurantEntity(**restaurant.dict())
        restaurant_entity.name = name

        return restaurant_entity
