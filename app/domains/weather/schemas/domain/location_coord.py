from pydantic import BaseModel


__all__ = [
    "LocationCoordSchema",
]


class LocationCoordSchema(BaseModel):
    """
    Schema for geographical coordinates.

    Attributes:
        lat: Latitude coordinate.
        lon: Longitude coordinate.
    """
    lat: float
    lon: float
