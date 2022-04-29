import os
from flask import Flask, render_template, request
from ipfs import upload_ipfs

UPLOAD_FOLDER = "./files"

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
                ipfs_hash = upload_ipfs(file_path, filename)
                os.remove(file_path)
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
            return render_template(
                "download.html",
                file_url=f"http://0.0.0.0:8080/ipfs/{ipfs_hash}",
            )
        return render_template("download.html")
    except Exception as e:
        print(e)
        return render_template("download.html", error=str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
