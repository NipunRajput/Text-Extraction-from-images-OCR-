from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import pytesseract
import easyocr
import ocrmypdf
import os
from PyPDF2 import PdfReader
import logging

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def tesseract_ocr(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        if not text:
            logger.warning(f"Tesseract OCR returned no text for image {image_path}")
        return text
    except pytesseract.pytesseract.TesseractNotFoundError:
        logger.error("Tesseract OCR is not installed or not found in your system PATH.")
        return "Tesseract OCR is not installed or not found in your system PATH."

def easyocr_ocr(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    text = ' '.join([res[1] for res in result])
    if not text:
        logger.warning(f"EasyOCR returned no text for image {image_path}")
    return text

def ocrmypdf_ocr(image_path):
    try:
        # Use ocrmypdf to convert image to PDF and then extract text
        output_pdf_path = image_path.replace('.png', '_ocr.pdf')
        ocrmypdf.ocr(image_path, output_pdf_path, image_dpi=300)
        # Extract text from the output PDF
        reader = PdfReader(output_pdf_path)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        if not text:
            logger.warning(f"OCRmyPDF returned no text for image {image_path}")
        return text
    except Exception as e:
        logger.error(f"OCRmyPDF encountered an error: {e}")
        return f"OCRmyPDF encountered an error: {e}"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logger.info(f"File saved to {filepath}")
            tesseract_text = tesseract_ocr(filepath)
            easyocr_text = easyocr_ocr(filepath)
            ocrmypdf_text = ocrmypdf_ocr(filepath)
            return render_template('index.html', tesseract_text=tesseract_text, easyocr_text=easyocr_text, ocrmypdf_text=ocrmypdf_text, image_path=f'uploads/{filename}')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
