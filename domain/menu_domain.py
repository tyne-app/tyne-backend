from loguru import logger
from dto.dto import GenericDTO as MenuDTO
from integration.integrations import MSBackboneMenu


async def get_menu(branch_id: int):
    ms_backbone_menu = MSBackboneMenu()
    menu_dto = MenuDTO()

    menu = await ms_backbone_menu.read_menu(branch_id=branch_id)

    if not menu:
        menu_dto.error = 'Error ms menu, respuesta en mejora'  # TODO:  Mejorar repsuesta
        return menu_dto.__dict__

    menu_dto.data = menu
    return menu_dto.__dict__


async def get_category_menu(branch_id: int):
    return None