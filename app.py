from flask import Flask, request, jsonify
import fitz  # PyMuPDF for PDFs
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

@app.route("/read_file", methods=["POST"])
def read_file():
    file = request.files['file']

    # Save temporarily
    filepath = os.path.join("/tmp", file.filename)
    file.save(filepath)

    text = ""
    if file.filename.endswith(".pdf"):
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()  # direct text
            if not page.get_text():  # OCR fallback
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img)
    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({"content": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

