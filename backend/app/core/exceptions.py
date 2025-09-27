from fastapi import HTTPException, status


class CustomException(HTTPException):
    """Base custom exception."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class AuthenticationException(CustomException):
    """Authentication exception."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AuthorizationException(CustomException):
    """Authorization exception."""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundException(CustomException):
    """Not found exception."""
    def __init__(self, detail: str = "Item not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ValidationException(CustomException):
    """Validation exception."""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class ConflictException(CustomException):
    """Conflict exception."""
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

