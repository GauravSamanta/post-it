class CustomException(Exception):
	"""Base class for custom exceptions."""

	def __init__(self, status_code: int, detail: str):
		self.status_code = status_code
		self.detail = detail
		super().__init__(detail)


class UserNotFoundException(CustomException):
	"""Raised when a user is not found in the database."""

	def __init__(self, detail: str = 'User not found.'):
		super().__init__(status_code=404, detail=detail)


class DuplicateUserException(CustomException):
	"""Raised when trying to create a user that already exists."""

	def __init__(self, detail: str = 'A user with this email already exists.'):
		super().__init__(status_code=409, detail=detail)
