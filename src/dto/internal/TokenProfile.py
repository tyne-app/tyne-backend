class TokenProfile:
    user_id: int
    email: str
    rol: int

    def __init__(self, user_id: int, email: str, rol: int):
        self.user_id = user_id
        self.email = email
        self.rol = rol
