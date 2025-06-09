import re

from pydantic import BaseModel, Field, field_validator


__all__ = [
    "FetchCityWeatherFiltersSchema",
]


class FetchCityWeatherFiltersSchema(BaseModel):
    """
    Filters used for filtering weather data.

    Attributes:
        city: City name with validation for format and content.
    """

    city: str = Field(
        description="City name",
        min_length=2,
        max_length=100,
        examples=["kyiv", "new york"],)

    @field_validator("city")
    @classmethod
    def validate_city_name(cls, val: str) -> str:
        """
        Validate and normalize city name input.

        Performs comprehensive validation including:
        - Empty value checks
        - Character set validation (letters, spaces, hyphens, apostrophes, dots)
        - Format validation (no multiple spaces, proper positioning of special chars)
        - Normalization to lowercase with single spaces

        Args:
            val: Raw city name input.

        Returns:
            str: Validated and normalized city name.

        Raises:
            ValueError: If city name format is invalid or contains forbidden characters.
        """
        if not val or not val.strip():
            raise ValueError("City name cannot be empty")

        val = val.strip()

        if not re.match(r"^[a-zA-ZÀ-ÿ\u0100-\u017F\u0400-\u04FF\s\-'\.]+$", val):
            raise ValueError(
                "City name can only contain letters, spaces, hyphens, "
                "apostrophes and dots. Numbers and special characters are not allowed."
            )

        if re.match(r"^[\s\-'\.]+$", val):
            raise ValueError("City name must contain at least one letter")

        suspicious_patterns = [
            r"\s{2,}",  # Multiple spaces
            r"^[\-'\.]+",  # Starts with a hyphen/dot/apostrophe
            r"[\-'\.]+$",  # Ends with a hyphen/dot/apostrophe
            r"[\-'\.]{2,}",  # Multiple special characters in a row
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, val):
                raise ValueError(f"Invalid city name format: '{val}'")

        return " ".join(word.lower() for word in val.split())
