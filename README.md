# QR Code to Phone Number Extractor

This is a web application built using **Flask** that extracts phone numbers from QR codes. It decodes the QR code to retrieve the phone number, identifies the country code, and displays the country name.

## Features
- Upload a QR code image.
- Extract phone number from the QR code.
- Get the country code and country name based on the phone number.
- Designed to run locally and deploy on platforms like Heroku.

## Requirements

This app requires Python 3.6+ and the following Python packages:

- Flask
- pyzbar
- phonenumbers
- Pillow

## Installation

### 1. Clone the repository
Clone this repository to your local machine:
```bash
git clone https://github.com/hzcv/qr-phone-extractor.git

cd qr-phone-extractor

python app.py
