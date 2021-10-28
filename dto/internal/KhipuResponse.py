class KhipuResponse:
    payment_id: str
    url: str
    status: int

    def __init__(self, url: str, payment_id: str, status: int):
        self.url = url
        self.payment_id = payment_id
        self.status = status
