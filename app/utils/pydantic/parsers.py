from typing import List, Dict, Any

from pydantic import ValidationError

__all__ = [
    "parse_validation_error",
]


def parse_validation_error(exc: ValidationError) -> List[Dict[str, Any]]:
    """
    Parse Pydantic validation error into structured format.

    Converts validation error into list of dictionaries with
    field locations, error messages, and error types.

    Args:
        exc: Pydantic validation error containing field errors.

    Returns:
        List[Dict[str, Any]]: List of error objects with loc, msg, and type fields.
    """
    return [{
        "loc": list(error.get("loc", [])),
        "msg": error.get("msg", ""),
        "type": error.get("type", "")
    } for error in exc.errors()]
