from src.domain2.Category import Category
from src.domain2.Product import Product
from src.domain2.SectionMenu import SectionMenu
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.ProductEntity import ProductEntity


class Menu:
    sections: list[SectionMenu]
    branch_id: str
    nombre_local: str
    rating: str
    rango_precio: []

    def __init__(self):
        self.sections = list()

    def to_menu_read_domain(self, products: list[ProductEntity], branch: BranchEntity):
        menu_domain = Menu()

        menu_domain.set_branch_id(branch)
        menu_domain.set_name(branch)
        menu_domain.set_sections_and_rango_precio(products)
        menu_domain.set_rating("")

        return menu_domain

    def set_branch_id(self, branch: BranchEntity):
        self.branch_id = branch.id

    def set_name(self, branch: BranchEntity):
        self.nombre_local = branch.restaurant.name

    def set_sections_and_rango_precio(self, products):
        price_set = list()

        for product in products:
            product_domain = Product(product.product_dict())
            category_domain = Category(product.get_category_dict())
            self.add_seccion(product_domain, category_domain)

            #  TODO: Desacoplar
            price_set.append(product.amount)
        max_amount = max(price_set, key=float)
        min_amount = min(price_set, key=float)
        avg_amount = sum(price_set) / len(price_set)
        self.rango_precio = {
            "max": max_amount,
            "min": min_amount,
            "avg": avg_amount,
        }

        return self

    def set_rating(self, opinions):
        qualifications = list()
        if opinions:
            for opt in list(opinions):
                qualifications.append(opt.qualification)
            self.rating = sum(qualifications) / len(qualifications)
            return self

        else:
            self.rating = 0
            return self

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
        return self

    def calculate_rango_precio(self):
        products = set()
        for sec in self.sections:
            products.add(sec.get_products())

        print(products)
