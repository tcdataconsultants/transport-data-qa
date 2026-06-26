from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

main = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "zip", "xml"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files.get("dataset_file")

        if not uploaded_file or uploaded_file.filename == "":
            return render_template("upload.html", error="No file selected.")

        if not allowed_file(uploaded_file.filename):
            return render_template("upload.html", error="Unsupported file type.")

        original_name = secure_filename(uploaded_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_name = f"{timestamp}_{original_name}"

        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
        saved_path = upload_folder / saved_name
        uploaded_file.save(saved_path)

        return redirect(url_for("main.upload_success", filename=saved_name))

    return render_template("upload.html")


@main.route("/upload/success")
def upload_success():
    filename = request.args.get("filename")
    return render_template("upload_success.html", filename=filename)