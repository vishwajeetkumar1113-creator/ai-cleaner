from flask import Flask, request, send_file
import cv2
import numpy as np
import tempfile

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "status": "running",
        "service": "AI Auto Crop API"
    }

@app.route("/clean", methods=["POST"])
def clean():

    file = request.files["file"]

    image = cv2.imdecode(
        np.frombuffer(file.read(), np.uint8),
        cv2.IMREAD_COLOR
    )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:

        largest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest)

        image = image[y:y+h, x:x+w]

    cleaned = cv2.detailEnhance(
        image,
        sigma_s=10,
        sigma_r=0.15
    )

    temp = tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    )

    cv2.imwrite(temp.name, cleaned)

    return send_file(
        temp.name,
        mimetype="image/jpeg"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0")
