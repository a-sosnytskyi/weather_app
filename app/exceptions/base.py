__all__ = [
    "NotFoundException",
    "BadRequestException",
    "BadGatewayException",
]


class NotFoundException(Exception):
    """Exception raised when requested resource is not found."""
    pass


class BadRequestException(Exception):
    """Exception raised for invalid client requests or parameters."""
    pass


class BadGatewayException(Exception):
    """Exception raised when external service is unavailable or returns errors."""
    pass
