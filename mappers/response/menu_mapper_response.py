from domain2.Category import Category
from domain2.Menu import Menu
from domain2.Product import Product
from domain2.SectionMenu import SectionMenu
from dto.dto import GenericDTO as wrapperDTO

from dto.response.MenuRespDTO import MenuRespDTO, CategoryRespDTO, SectionMenuRespDTO, ProductRespDTO
from loguru import logger

from repository.entity.ProductEntity import ProductEntity


def to_menu_read_response(menu: Menu):
    # wrapper_response = wrapperDTO()

    menu_response = to_menu_response(menu)

    # wrapper_response.data = to_menu_response(menu)

    # return wrapper_response.__dict__

    return menu_response


def to_menu_create_response():
    wrapper_response = wrapperDTO()
    menu = Menu()

    wrapper_response.data = [{"details": "Productos guardados correctamente"}]

    return wrapper_response.__dict__


def to_category_response(category: Category):
    category_resp = CategoryRespDTO

    category_resp.id = category.id
    category_resp.name = category.name

    return category_resp


def to_product_response(products: list[Product]):
    products_resp = list()

    for product in products:
        product_resp = ProductRespDTO

        product_resp.id = product.id
        product_resp.name = product.name
        product_resp.description = product.description
        product_resp.url_image = product.url_image
        product_resp.amount = product.amount
        product_resp.commision_tyne = product.commission_tyne

        products_resp.append(product_resp)

    return products_resp


def to_section_response(section: SectionMenu):
    section_resp = SectionMenuRespDTO

    section_resp.category = to_category_response(section.category)
    section_resp.products = to_product_response(section.products)

    return section_resp


def to_menu_response(menu: Menu):
    menu_resp = MenuRespDTO
    sections_resp = list()

    for section in menu.sections:
        section_resp = to_section_response(section)
        sections_resp.append(section_resp)

    menu_resp.sections = sections_resp

    return menu_resp
