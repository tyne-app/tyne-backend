from unicodedata import category

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

    def to_menu_read_domain(self, products: list[ProductEntity], branch, categories):
        menu_domain = Menu()
        menu_domain.set_branch_id(branch)
        menu_domain.set_name(branch)
        menu_domain.set_sections_and_rango_precio(products, categories)
        menu_domain.set_rating("")

        return menu_domain

    def set_branch_id(self, branch: BranchEntity):
        self.branch_id = branch.id

    def set_name(self, branch: BranchEntity):
        self.nombre_local = branch.name

    def set_sections_and_rango_precio(self, products, categories):
        price_set = list()
        max_amount = 0
        min_amount = 0
        avg_amount = 0
        self.create_section(categories)
        for category in categories:
            for product in products:
                if product.category.id == category.id:
                    product_domain = Product(product.product_dict())
                    price_set.append(product.amount)
                    self.add_seccion(product_domain, category)

        if len(price_set) > 0:
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
        for seccion in self.sections:
            if category.id == seccion.category.id:
                if product:
                    seccion.add_product(product)

    def create_section(self, categories):
        for category in categories:
            section = SectionMenu(None, category)
            self.sections.append(section)
        return self

    def calculate_rango_precio(self):
        products = set()
        for sec in self.sections:
            products.add(sec.get_products())
