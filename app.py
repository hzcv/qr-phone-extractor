from flask import Flask, render_template_string, request
import phonenumbers
import cv2
from PIL import Image
import os

app = Flask(__name__)

# Define folder for storing uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Function to check if file is an allowed image
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract phone number from the QR code using OpenCV
def extract_phone_number_from_qr(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect QR code in the image
    detector = cv2.QRCodeDetector()
    value, pts, qr_code = detector(gray)
    if value:
        return value
    return None

# Function to get country info from phone number
def get_country_info(phone_number):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number)
        
        # Get the country code
        country_code = parsed_number.country_code
        # Get the country name using phonenumbers
        region_code = phonenumbers.region_code_for_number(parsed_number)
        
        # Fetch the full country name
        from phonenumbers import geocoder
        country_name = geocoder.description_for_number(parsed_number, "en")

        return country_code, country_name

    except phonenumbers.phonenumberutil.NumberParseException as e:
        return None, "Error parsing phone number"

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Phone Number Extractor</title>
</head>
<body>
    <h1>Upload QR Code Image</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <label for="file">Select QR code image:</label>
        <input type="file" name="file" id="file" accept="image/*" required>
        <br><br>
        <button type="submit">Upload Image</button>
    </form>

    {% if phone_number %}
    <h2>Extracted Phone Number Details</h2>
    <p><strong>Phone Number:</strong> {{ phone_number }}</p>
    <p><strong>Country Code:</strong> +{{ country_code }}</p>
    <p><strong>Country:</strong> {{ country_name }}</p>
    {% elif error %}
    <p style="color:red">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

# Route for the main page with the form
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route to handle the uploaded file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template_string(HTML_TEMPLATE, error="No file part")

    file = request.files['file']
    
    if file.filename == '':
        return render_template_string(HTML_TEMPLATE, error="No selected file")
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Extract phone number from the uploaded image
        phone_number = extract_phone_number_from_qr(filename)
        
        if phone_number:
            country_code, country_name = get_country_info(phone_number)
            return render_template_string(HTML_TEMPLATE, phone_number=phone_number, country_code=country_code, country_name=country_name)
        else:
            return render_template_string(HTML_TEMPLATE, error="No phone number found in the QR code")
    else:
        return render_template_string(HTML_TEMPLATE, error="Invalid file format. Please upload a valid image.")

if __name__ == '__main__':
    # Create 'uploads' folder if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # Run the app on all available network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)
