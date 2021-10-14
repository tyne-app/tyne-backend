# TODO: Convertir a Schemas de respuesta
"""
class ProductDTO:
    id: str
    name: str
    description: str
    url_image: str
    amount: str
    commision_tyne: str

    def __init__(self, product_json):
        self.id = product_json["id"]
        self.name = product_json["name"]
        self.description = product_json["description"]
        self.url_image = product_json["image_url"]
        self.amount = product_json["amount"]
        self.commision_tyne = product_json["commision_tyne"]


class CategoryDTO:
    id: str
    name: str

    def __init__(self, cat_json):
        self.id = cat_json["id"]
        self.name = cat_json["name"]


class SectionMenuDTO:
    category: CategoryDTO
    products: [ProductDTO]

    def __init__(self, product: ProductDTO, category: CategoryDTO):
        self.category = category
        self.products = list()
        self.products.append(product)

    def is_exit(self, category: CategoryDTO):
        return self.category.id == category.id

    def add_product(self, product: ProductDTO):
        self.products.append(product)


class MenuDTO:
    menu: list[SectionMenuDTO]

    def __init__(self):
        self.menu = list()

    def add_seccion(self, product: ProductDTO, category: CategoryDTO):

        # Verificar si no existe ninguna Seccion
        if self.menu.__len__() == 0:
            return self.create_section(category, product)

        # Validar si la seccion es la misma
        # Si es la misma, agregar Product a dicha Seccion
        for seccion in self.menu:
            if seccion.is_exit(category):
                seccion.add_product(product)
                return seccion

        # Si no, crear la Seccion
        return self.create_section(category, product)

    def create_section(self, categoryDTO, productDTO):
        section = SectionMenuDTO(productDTO, categoryDTO)
        self.menu.append(section)
        return section
"""
