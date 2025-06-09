from pydantic import ValidationError

__all__ = [
    "parse_validation_error",
]


def parse_validation_error(exc: ValidationError) -> str:
    """
    Parse Pydantic validation error into human-readable string.

    Converts validation error with field locations and messages
    into a formatted string with field paths and error descriptions.

    Args:
        exc: Pydantic validation error containing field errors.

    Returns:
        str: Formatted error string with field paths and messages.
    """
    return "; ".join(f"{' -> '.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in exc.errors())
