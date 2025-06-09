from pydantic import BaseModel
from typing import List, Optional


__all__ = [
    "WeatherResponseSchema",
]


class Coordinates(BaseModel):
    """Geographic coordinates"""
    lon: float
    lat: float


class Weather(BaseModel):
    """Weather condition details"""
    id: int
    main: str
    description: str
    icon: str


class MainWeather(BaseModel):
    """Main weather parameters"""
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class Wind(BaseModel):
    """Wind information"""
    speed: float
    deg: int
    gust: Optional[float] = None


class Clouds(BaseModel):
    """Cloudiness information"""
    all: int


class SystemInfo(BaseModel):
    """System information"""
    type: Optional[int] = None
    id: Optional[int] = None
    country: str
    sunrise: int
    sunset: int


class WeatherResponseSchema(BaseModel):
    """Complete weather API response"""
    coord: Coordinates
    weather: List[Weather]
    base: str
    main: MainWeather
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: SystemInfo
    timezone: int
    id: int
    name: str
    cod: int
