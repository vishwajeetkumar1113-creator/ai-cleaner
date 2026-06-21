from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


@app.route("/")
def home():
    return {
        "status": "running",
        "service": "Cyber Cafe AI Crop API"
    }


@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image uploaded"
        })

    file = request.files["image"]

    original_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(original_path)

    image = cv2.imread(original_path)

    if image is None:
        return jsonify({
            "success": False,
            "error": "Invalid image"
        })

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    largest = None
    max_area = 0

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > max_area:
            max_area = area
            largest = cnt

    if largest is not None:

        x, y, w, h = cv2.boundingRect(
            largest
        )

        cropped = image[
            y:y+h,
            x:x+w
        ]

        crop_name = (
            "crop_" +
            file.filename
        )

        crop_path = os.path.join(
            UPLOAD_FOLDER,
            crop_name
        )

        cv2.imwrite(
            crop_path,
            cropped
        )

        return jsonify({
            "success": True,
            "filename": file.filename,
            "cropped": crop_name,
            "cropped_url":
                request.host_url +
                "uploads/" +
                crop_name,
            "width": w,
            "height": h
        })

    return jsonify({
        "success": False,
        "error": "Document not detected"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
