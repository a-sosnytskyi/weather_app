import sys
from pathlib import Path

import uvicorn

# Add the project root directory to the Python path (necessary for correct module importing)
sys.path.append(str(Path(__file__).parent.parent))

from app.kernel.app_factory import AppFactory
from app.kernel.settings import app_settings

app = AppFactory.configure()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=app_settings.app_port,
        reload=app_settings.app_reload,
        reload_dirs=["/app"]
    )
