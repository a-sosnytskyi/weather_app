from typing import Optional

from fastapi import FastAPI
from pydantic import ValidationError

from app.infrastructure.cache import RedisCacheManager
from app.kernel.settings import app_settings


class AppFactory:
    """
    Application factory for creating the FastAPI application.
    """

    def __init__(self, app: FastAPI):
        self.app: FastAPI = app

    @classmethod
    def configure(cls, app: Optional[FastAPI] = None) -> FastAPI:
        """
        Initialize and configure the FastAPI application.

        Sets up exception handlers, startup/shutdown events, and API routing.

        Args:
            app: Optional FastAPI instance to configure (creates new if None).

        Returns:
            FastAPI: Fully configured FastAPI application.
        """
        _app = app or FastAPI(debug=app_settings.debug)
        instance = cls(app=_app)

        # if not app_settings.debug:
        #     instance.register_exception_handlers()
        instance.register_exception_handlers()

        instance.attach_app_startup_events()
        instance.attach_app_shutdown_events()
        return instance.app

    def attach_app_startup_events(self):
        """
        Attach app startup events to the FastAPI application.

        Registers API routing and Redis cache initialization on startup.
        """
        self.app.add_event_handler("startup", self.attach_api)
        self.app.add_event_handler("startup", RedisCacheManager.initialize)

    def attach_app_shutdown_events(self):
        """
        Attach app shutdown events to the FastAPI application.

        Registers Redis cache cleanup on application shutdown.
        """
        self.app.add_event_handler("shutdown", RedisCacheManager.cleanup)

    def attach_api(self):
        """Attach API endpoints to the FastAPI application instance."""
        from app.api.v1 import api_router_v1
        self.app.include_router(api_router_v1, prefix="/api/v1")

    def register_exception_handlers(self):
        """
        Register global exception handlers for the application.

        Maps custom exceptions and validation errors to appropriate HTTP responses.
        """
        from app.api import exception_handlers
        from app.exceptions import NotFoundException, BadRequestException, BadGatewayException

        self.app.add_exception_handler(ValidationError, exception_handlers.pyd_validation_exception_handler)
        self.app.add_exception_handler(NotFoundException, exception_handlers.not_found_exception_handler)
        self.app.add_exception_handler(BadRequestException, exception_handlers.bad_request_exception_handler)
        self.app.add_exception_handler(BadGatewayException, exception_handlers.bad_gateway_exception_handler)
        self.app.add_exception_handler(ValueError, exception_handlers.bad_request_exception_handler)
        self.app.add_exception_handler(TypeError, exception_handlers.unexcpected_code_error_exception_handler)
        self.app.add_exception_handler(Exception, exception_handlers.unexcpected_code_error_exception_handler)
