from fastapi import Request
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from app.exceptions import NotFoundException, BadRequestException, BadGatewayException
from app.utils.pydantic import parse_validation_error


async def pyd_validation_exception_handler(request: Request, exc: ValidationError) -> Response:
    """
    Handle Pydantic validation errors.

    Returns:
        Response: JSON response with 422 status and formatted validation error msg.
    """
    return JSONResponse(
        status_code=422,
        content={"detail": parse_validation_error(exc)},
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException) -> Response:
    """
    Handle resource not found errors.

    Returns:
        Response: JSON response with 404 status and error message.
    """
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


async def bad_request_exception_handler(request: Request, exc: BadRequestException | ValueError) -> Response:
    """
    Handle bad request and value errors.

    Returns:
        Response: JSON response with 400 status and error message.
    """
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


async def bad_gateway_exception_handler(request: Request, exc: BadGatewayException) -> Response:
    """
    Handle bad gateway errors from external services.

    Returns:
        Response: JSON response with 502 status and error message.
    """
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)}
    )


async def unexcpected_code_error_exception_handler(request: Request, exc: Exception | TypeError) -> Response:
    """
    Handle unexpected server errors and type errors.

    Returns:
        Response: JSON response with 500 status and error message.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
