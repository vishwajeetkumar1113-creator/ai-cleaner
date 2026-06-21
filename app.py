from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return {
        "status": "running",
        "service": "Cyber Cafe AI Crop API"
    }

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    img = Image.open(path)

    width, height = img.size

    return jsonify({
        "success": True,
        "filename": file.filename,
        "width": width,
        "height": height
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
