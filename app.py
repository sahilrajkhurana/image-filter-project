from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # Get uploaded image
        file = request.files['image']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Read image and convert to grayscale
        image = cv2.imread(filepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Get selected filter from dropdown (STEP 3.2)
        selected_filter = request.form.get("filter")

        # Initialize output paths
        mean_path = gaussian_path = laplacian_path = None

        # Apply Mean Filter
        if selected_filter in ["mean", "all"]:
            mean_img = cv2.blur(gray, (3, 3))
            mean_path = 'static/mean.jpg'
            cv2.imwrite(mean_path, mean_img)

        # Apply Gaussian Filter
        if selected_filter in ["gaussian", "all"]:
            gaussian_img = cv2.GaussianBlur(gray, (3, 3), 1)
            gaussian_path = 'static/gaussian.jpg'
            cv2.imwrite(gaussian_path, gaussian_img)

        # Apply Laplacian Filter
        if selected_filter in ["laplacian", "all"]:
            laplacian_img = cv2.Laplacian(gray, cv2.CV_64F)
            laplacian_img = cv2.convertScaleAbs(laplacian_img)
            laplacian_path = 'static/laplacian.jpg'
            cv2.imwrite(laplacian_path, laplacian_img)

        return render_template(
            'index.html',
            original=filepath,
            mean=mean_path,
            gaussian=gaussian_path,
            laplacian=laplacian_path
        )

    return render_template('index.html')


# Required for Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)






