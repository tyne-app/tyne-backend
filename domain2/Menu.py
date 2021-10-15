from domain2.Category import Category
from domain2.Product import Product
from domain2.SectionMenu import SectionMenu


class Menu:
    sections: list[SectionMenu]

    def __init__(self):
        self.sections = list()

    def add_seccion(self, product: Product, category: Category):

        # Verificar si no existe ninguna Seccion
        if self.sections.__len__() == 0:
            return self.create_section(category, product)

        # Validar si la seccion es la misma
        # Si es la misma, agregar Product a dicha Seccion
        for seccion in self.sections:
            if seccion.is_exit(category):
                seccion.add_product(product)
                return seccion

        # Si no, crear la Seccion
        return self.create_section(category, product)

    def create_section(self, category, product):
        section = SectionMenu(product, category)
        self.sections.append(section)
        return section
