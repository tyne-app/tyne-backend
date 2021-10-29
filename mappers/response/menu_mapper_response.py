from domain2.Menu import Menu
from dto.dto import GenericDTO as wrapperDTO

from repository.entity.BranchEntity import BranchEntity
from repository.entity.ProductEntity import ProductEntity


def to_menu_read_response(products: list[ProductEntity], branch: BranchEntity, opinions):
    response = wrapperDTO()
    response.data = Menu.to_menu_read_domain(products, branch, opinions)
    return response.__dict__


def to_menu_create_response():
    response = wrapperDTO()
    response.data = [{"message": "Menu creado correctamente"}]
    return response.__dict__
