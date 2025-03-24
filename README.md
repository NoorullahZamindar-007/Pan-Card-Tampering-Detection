# Pan-Card-Tampering-Detection
A Flask web app for detecting PAN card tampering using SSIM and OpenCV.

# 📝 PAN Card Tampering Detection

PAN Card Tampering Detection is a Flask web application that detects tampering in PAN card images using SSIM (Structural Similarity Index) and OpenCV. It allows users to upload an original and a tampered image, and then visually highlights the differences between them.

---

## 🚀 Features
- Upload two images (original and tampered) via a web interface.
- Automatically resize and process images to ensure compatibility.
- Calculate the Structural Similarity Index (SSIM) between the two images.
- Highlight the differences by drawing bounding boxes around tampered areas.
- Display both the original and tampered images with contours.
- Responsive and modern user interface using **Bootstrap**.
- Supports all major image formats (PNG, JPG, JPEG).

---

## 🖥️ Technologies Used
- **Python**: Core language for backend processing.
- **Flask**: Web framework for creating the application.
- **OpenCV**: Image processing and contour detection.
- **scikit-image**: Structural Similarity Index (SSIM) calculation.
- **Bootstrap**: Modern, responsive web design.
- **HTML/CSS**: Frontend design and layout.

---

