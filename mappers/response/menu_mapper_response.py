from domain2.Category import Category
from domain2.Menu import Menu
from domain2.Product import Product
from dto.dto import GenericDTO as wrapperDTO
from dto.response.MenuResponseDTO import MenuResponseDTO
from loguru import logger

from repository.entity.ProductEntity import ProductEntity


def to_menu_read_response(menu: Menu):
    wrapper_response = wrapperDTO()
    menu_response = MenuResponseDTO

    for section in menu.sections:
        logger.info(section)

    wrapper_response.data = menu_response

    return wrapper_response.__dict__


def to_menu_create_response():
    wrapper_response = wrapperDTO()
    menu = Menu()

    wrapper_response.data = [{"details": "Productos guardados correctamente"}]

    return wrapper_response.__dict__
