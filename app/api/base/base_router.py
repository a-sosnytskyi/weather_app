from typing import List

from fastapi import APIRouter


class BaseAPIRouteWrapper:
    """
    Base class for creating API routers.
    """
    router: APIRouter
    children_routers: List["BaseAPIRouteWrapper"] = []

    @classmethod
    def collect_router(cls):
        """
        Collects and includes all child routers into the main router of the class.

        This class method iterates over all routers defined in the `children_routers` attribute
        and includes each one into the main router (`cls.router`) of the class. This is useful for
        modular API structures, where multiple sub-routers are defined and need to be aggregated
        into a single router that can be registered with the FastAPI app.

        Returns:
            APIRouter: The main router of the class with all child routers included.
        """
        for child_router in cls.children_routers:
            cls.router.include_router(child_router.router)
        return cls.router
