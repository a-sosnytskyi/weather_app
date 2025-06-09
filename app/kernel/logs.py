import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Literal

from app.kernel.settings import app_settings


def colorize_text(
        text: str,
        color: Literal[
            "red", "green", "yellow", "blue", "magenta", "cyan", "light_grey",
            "bright_red", "bright_green", "bright_yellow", "bright_blue", "reset"
        ] = "reset"
) -> str:
    """
    Colorize text for terminal output

    Args:
        text (str): Text to colorize
        color (str): Color name

    Returns:
        str: Colorized text
    """
    color_codes = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "light_grey": "\033[37m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "reset": "\033[0m",
    }
    color_prefix = color_codes.get(color, '')
    color_suffix = color_codes['reset']
    return f"{color_prefix}{text}{color_suffix}"


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log messages based on level
    """

    COLOR_ALIASES = {
        "DEBUG": "light_grey",
        "INFO": "reset",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bright_red",
    }

    def format(self, record):
        # Get color for this level
        levelname = record.levelname
        color_alias = self.COLOR_ALIASES.get(levelname, self.COLOR_ALIASES["INFO"])

        # Format with original formatter
        formatted_message = super().format(record)

        # Return colored version
        return colorize_text(text=formatted_message, color=color_alias)


def configure_logger():
    log_dir = f"{app_settings.root_dir}/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = f"{log_dir}/app.log"
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    _logger = logging.getLogger("fastapi")
    _logger.setLevel(app_settings.log_level)

    # TERMINAL LOGS
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(log_format))
    _logger.addHandler(console_handler)

    # FILE LOGS
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(log_format))
    _logger.addHandler(file_handler)

    # remove logger duplications
    _logger.propagate = False
    return _logger


logger = configure_logger()


__all__ = ["logger"]
