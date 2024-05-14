'''
---main.py---
For backend setup, routes, uploading file etc.
Use different file for pdf analysis, grammar check etc.
Todo: Improve uploading, see: https://flask.palletsprojects.com/en/3.0.x/patterns/fileuploads/
'''
import os
from flask import Flask, request, jsonify
from typing import List, Union
from app.pdf_analysis import process_pdf, extract_text_from_pdf, count_pages, compare_pages
import fitz

app = Flask(__name__)

# Upload the file, then call the analysis functions
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file to a folder named 'uploads'
        upload_folder = os.path.join(app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Extract text content and analyze PDF
        text_content, text_blocks, pages = process_pdf(file_path)

        text = extract_text_from_pdf(file_path)

        pages = count_pages(file_path)

        stated_number_of_pages = compare_pages(text, pages)

        # Removes the file after analysis
        # Perhaps find a different way to do this in prod
        # Preferably something with a timer
        os.remove(file_path)

        return jsonify({
            'message': 'File uploaded successfully',
            'file_name': file.filename,
            'file_path': file_path,
            'text_blocks': text_blocks,
            'pages_amount': pages,
            'text_content': text,
            'stated_equals_actual' : stated_number_of_pages

        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Keep root at bottom
@app.route("/")
def read_root():
    return {"message": "Hello, World!"}
