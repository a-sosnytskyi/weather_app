from pathlib import Path

from pydantic_settings import BaseSettings


class SettingsApp(BaseSettings):
    """
    Application settings for the application.

    Attributes:
        debug: Whether the application is running in debug mode.
        app_port: The port for the application on which the server is running.
        app_reload: Whether to enable auto-reload in development.
    """
    debug: bool = False
    app_port: int = 8000
    app_reload: bool = False

    @property
    def app_dir(self):
        return Path(__file__).parent.parent.parent

    @property
    def root_dir(self):
        return self.app_dir.parent


app_settings = SettingsApp()
