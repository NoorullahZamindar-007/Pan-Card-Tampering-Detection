from flask import Flask, request, render_template, redirect, url_for
import cv2
import imutils
from skimage.metrics import structural_similarity as ssim
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.static_folder = 'uploads'



# Function to compare images and find differences
def compare_images(original_path, tampered_path):
    # Load the images
    original = cv2.imread(original_path)
    tampered = cv2.imread(tampered_path)

    # Resize the tampered image to match the original image size
    tampered = cv2.resize(tampered, (original.shape[1], original.shape[0]))

    # Convert the images to grayscale
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    tampered_gray = cv2.cvtColor(tampered, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    (score, diff) = ssim(original_gray, tampered_gray, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Find contours to locate the differences
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Draw bounding boxes on both images
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(original, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(tampered, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Save the result images
    result_original = os.path.join(app.config['UPLOAD_FOLDER'], "result_original.png")
    result_tampered = os.path.join(app.config['UPLOAD_FOLDER'], "result_tampered.png")
    cv2.imwrite(result_original, original)
    cv2.imwrite(result_tampered, tampered)

    return score, result_original, result_tampered


# Route to upload images
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_file = request.files['original']
        tampered_file = request.files['tampered']

        if original_file and tampered_file:
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_file.filename)
            tampered_path = os.path.join(app.config['UPLOAD_FOLDER'], tampered_file.filename)

            original_file.save(original_path)
            tampered_file.save(tampered_path)

            # Compare the images
            score, result_original, result_tampered = compare_images(original_path, tampered_path)

            return render_template('index.html', score=score, original=result_original, tampered=result_tampered)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
