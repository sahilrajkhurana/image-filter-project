from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get uploaded image
        file = request.files['image']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Read image using OpenCV
        image = cv2.imread(filepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply filters
        mean_img = cv2.blur(gray, (3, 3))
        gaussian_img = cv2.GaussianBlur(gray, (3, 3), 1)
        laplacian_img = cv2.Laplacian(gray, cv2.CV_64F)

        # Save output images
        cv2.imwrite('static/mean.jpg', mean_img)
        cv2.imwrite('static/gaussian.jpg', gaussian_img)
        cv2.imwrite('static/laplacian.jpg', laplacian_img)

        return render_template(
            'index.html',
            original=filepath,
            mean='static/mean.jpg',
            gaussian='static/gaussian.jpg',
            laplacian='static/laplacian.jpg'
        )

    return render_template('index.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



