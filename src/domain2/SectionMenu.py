from src.domain2.Category import Category
from src.domain2.Product import Product


class SectionMenu:
    category: Category
    products: [Product]

    def __init__(self, product: Product, category: Category):
        self.category = category
        self.products = list()
        if product:
            self.products.append(product)

    def is_exit(self, category: Category):
        return self.category.id == category.id

    def add_product(self, product: Product):
        self.products.append(product)

    def get_products(self):
        return self.products
