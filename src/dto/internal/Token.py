class Token:
    id_user: int
    id_branch_client: int
    rol: int
    name: str
    last_name: str

    def __init__(self, id_user: int, id_branch_client: int):
        self.id_user = id_user
        self.id_branch_client = id_branch_client
