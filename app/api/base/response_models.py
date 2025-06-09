from pydantic import BaseModel


__all__ = [
    "BaseErrorRSchema",
    "BaseMessageRSchema",
]


class BaseErrorRSchema(BaseModel):
    """Base response schema for error messages.

    Attributes:
        detail: Error description message.
    """
    detail: str


class BaseMessageRSchema(BaseModel):
    """Base response schema for success messages.

    Attributes:
        message: Success or informational message content.
    """
    message: str
