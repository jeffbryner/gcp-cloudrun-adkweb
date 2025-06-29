import os

import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Example session DB URL (e.g., SQLite)
SESSION_DB_URL = "sqlite:///./sessions.db"
# Example allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]


# Call the function to get the FastAPI app instance
# set web to false since we will setup our own web collateral
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=False,
)

# add the web bits
import mimetypes
from fastapi.responses import RedirectResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles

mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("text/javascript", ".js", True)

BASE_DIR = Path(__file__).parent.resolve()
ANGULAR_DIST_PATH = BASE_DIR / "web_ui"


@app.get("/")
async def redirect_root_to_dev_ui():
    return RedirectResponse("/ui/")


@app.get("/ui")
async def redirect_dev_ui_add_slash():
    return RedirectResponse("/ui/")


app.mount(
    "/ui/",
    StaticFiles(directory=ANGULAR_DIST_PATH, html=True),
    name="static",
)


if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
