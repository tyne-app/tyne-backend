class Product:
    id: str
    name: str
    description: str
    url_image: str
    amount: str
    commission_tyne: str

    def __init__(self, product_json):
        self.id = product_json["id"]
        self.name = product_json["name"]
        self.description = product_json["description"]
        self.url_image = product_json["image_url"]
        self.amount = product_json["amount"]

    def get_amount(self):
        return self.amount
