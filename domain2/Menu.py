from domain2.Category import Category
from domain2.Product import Product
from domain2.SectionMenu import SectionMenu


class Menu:
    sections: list[SectionMenu]
    branch_id: str
    nombre_local: str
    rating: str
    rango_precio: []

    def __init__(self, branch_id: '', nombre_local: '', rating=None, rango_precio=None):
        self.sections = list()
        self.branch_id = branch_id
        self.nombre_local = nombre_local
        self.rating = rating
        self.rango_precio = rango_precio

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

    def calculate_rango_precio(self):
        products = set()
        for sec in self.sections:
            products.add(sec.get_products())

        print(products)
