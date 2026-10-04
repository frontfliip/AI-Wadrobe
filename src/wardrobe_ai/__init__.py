"""Personal wardrobe backend prototype."""

import os
from pathlib import Path

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config["DATA_DIR"] = Path(os.getenv("WARDROBE_DATA_DIR", "data")).resolve()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
