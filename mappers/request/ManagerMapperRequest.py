from loguru import logger
from dto.request.local_request_dto import Manager
from repository.entity.ManagerEntity import ManagerEntity


class ManagerMapperRequest:

    def to_manager_entity(self, manager: Manager):
        logger.info('manager: {}', manager)
        manager_dict = manager.dict()
        del(manager_dict['password'])
        manager_entity = ManagerEntity(**manager_dict)
        return manager_entity
