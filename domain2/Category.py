class Category:
    id: str
    name: str

    def __init__(self, cat_json):
        self.id = cat_json["id"]
        self.name = cat_json["name"]
