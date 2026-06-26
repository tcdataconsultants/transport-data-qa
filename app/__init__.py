from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "transport-data-qa"
    app.config["UPLOAD_FOLDER"] = Path("uploads")
    app.config["REPORT_FOLDER"] = Path("reports")

    app.config["UPLOAD_FOLDER"].mkdir(exist_ok=True)
    app.config["REPORT_FOLDER"].mkdir(exist_ok=True)

    from .routes import main
    app.register_blueprint(main)

    return app