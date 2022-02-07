class CustomError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.name = kwargs.get('name')
        self.detail = kwargs.get('detail')
        self.cause = kwargs.get('cause')
        self.status_code = kwargs.get('status_code')
