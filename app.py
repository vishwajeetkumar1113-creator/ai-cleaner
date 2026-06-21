from flask import Flask, request, send_file
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/clean", methods=["POST"])
def clean():

    file = request.files["file"]

    image = cv2.imdecode(
        np.frombuffer(file.read(), np.uint8),
        cv2.IMREAD_COLOR
    )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cleaned = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    cv2.imwrite("clean.jpg", cleaned)

    return send_file(
        "clean.jpg",
        mimetype="image/jpeg"
    )

if __name__ == "__main__":
    app.run()