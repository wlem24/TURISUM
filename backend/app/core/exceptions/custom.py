from fastapi import status


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class SpotNotFound(AppException):
    def __init__(self, spot_id: str = ""):
        super().__init__(f"Spot not found: {spot_id}", status.HTTP_404_NOT_FOUND)


class UserNotFound(AppException):
    def __init__(self, identifier: str = ""):
        super().__init__(f"User not found: {identifier}", status.HTTP_404_NOT_FOUND)


class GuideNotFound(AppException):
    def __init__(self):
        super().__init__("Guide not found", status.HTTP_404_NOT_FOUND)


class HotelNotFound(AppException):
    def __init__(self):
        super().__init__("Hotel not found", status.HTTP_404_NOT_FOUND)


class BookingNotFound(AppException):
    def __init__(self):
        super().__init__("Booking not found", status.HTTP_404_NOT_FOUND)


class UnauthorizedRole(AppException):
    def __init__(self, required: str = ""):
        super().__init__(
            f"Insufficient permissions. Required role: {required}",
            status.HTTP_403_FORBIDDEN,
        )


class InvalidCredentials(AppException):
    def __init__(self):
        super().__init__("Invalid email or password", status.HTTP_401_UNAUTHORIZED)


class EmailAlreadyExists(AppException):
    def __init__(self, email: str = ""):
        super().__init__(f"Email already registered: {email}", status.HTTP_409_CONFLICT)


class InvalidToken(AppException):
    def __init__(self):
        super().__init__("Invalid or expired token", status.HTTP_401_UNAUTHORIZED)


class SpotNotApproved(AppException):
    def __init__(self):
        super().__init__("Spot is not approved", status.HTTP_400_BAD_REQUEST)


class InvalidCoordinates(AppException):
    def __init__(self):
        super().__init__(
            "Coordinates must be within Saudi Arabia bounds",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
