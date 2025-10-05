class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class DuplicateUserException(CustomException):
    def __init__(self, detail: str = 'A user with this email already exists.'):
        super().__init__(status_code=409, detail=detail)
