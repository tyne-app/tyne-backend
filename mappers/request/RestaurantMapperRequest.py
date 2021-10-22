from loguru import logger
from dto.request.local_request_dto import Restaurant
from repository.entity.RestaurantEntity import RestaurantEntity


class RestaurantMapperRequest:

    def to_restaurant_entity(self, restaurant: Restaurant, name: str):
        logger.info('restaurant: {}', restaurant)

        restaurant_entity = RestaurantEntity(**restaurant.dict())
        restaurant_entity.name = name

        return restaurant_entity
