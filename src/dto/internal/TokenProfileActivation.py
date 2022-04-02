class TokenProfileActivation:
    email: str
    rol: int
    name: str
    last_name: str

    def __init__(self, email: str, rol: int, name: str, last_name: str):
        self.email = email
        self.rol = rol
        self.name = name
        self.last_name = last_name
