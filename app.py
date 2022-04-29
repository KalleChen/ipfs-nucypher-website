import os
import shutil
from flask import Flask, render_template, request, url_for, send_from_directory
from ipfs import upload_ipfs
from encrypt import encrypt_file
from decrypt import decrypt_file

UPLOAD_FOLDER = "./files"
PUBLIC_IP = "http://172.20.10.3:8080"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["POST", "GET"])
def index():
    try:
        if request.method == "POST":
            file = request.files["upload_file"]
            filename = file.filename
            if file and filename:
                print(file)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                encrypt_file(file_path, filename)
                ipfs_hash = upload_ipfs()
                shutil.rmtree("files")
                os.mkdir("files")
                return render_template("index.html", ipfs_hash=ipfs_hash)
    except Exception as e:
        print(e)
        return render_template("index.html", error=str(e))
    return render_template("index.html")


@app.route("/download", methods=["GET"])
def download():
    try:
        if "file_hash" in request.values:
            ipfs_hash = request.values["file_hash"]
            if not ipfs_hash:
                return render_template("download.html")
            file_name = decrypt_file(f"{PUBLIC_IP}/ipfs/{ipfs_hash}")
            return render_template(
                "download.html",
                file_url=url_for("download_file", filename=file_name),
            )
        return render_template("download.html")
    except Exception as e:
        print(e)
        return render_template("download.html", error=str(e))


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
