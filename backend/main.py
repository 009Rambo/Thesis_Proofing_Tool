'''
---main.py---
For backend setup, routes, uploading file etc.
Use different file for pdf analysis, grammar check etc.
Todo: Improve uploading, see: https://flask.palletsprojects.com/en/3.0.x/patterns/fileuploads/
'''
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from typing import List, Union
from app.pdf_analysis import process_pdf, extract_text_from_pdf, count_pages, compare_pages, extract_referenced_authors, search_referenced_authors_in_text, find_referenced_urls
import fitz
from app.crawler import Crawler
ALLOWED_EXTENSIONS = {"pdf", "docx"} # update as needed

app = Flask(__name__)

# Check if the uploaded files filetype is in the allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload the file, then call the analysis functions
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

       # if file is not allowed_file(file.filename):
        #    return jsonify({'error': 'Filetype not allowed'}), 400

        if file:       
            # Save the uploaded file to a folder named 'uploads'
            '''
            upload_folder = os.path.join(app.root_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)

            secured_file = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, secured_file)
            file.save(file_path)
            '''
            pdf_file = fitz.open(stream=file.read(), filetype="pdf")
            # Extract text content and analyze PDF
            text_content, text_blocks, pages = process_pdf(pdf_file)

            # Extract referenced author names from the reference list
            referenced_authors = extract_referenced_authors(text_content)

            # Search for referenced author names in the actual text
            found_authors = search_referenced_authors_in_text(text_content, referenced_authors)

            # Count pages and compare with stated number of pages
            stated_number_of_pages = compare_pages(text_content, pages)

            # Removes the file after analysis
            # Perhaps find a different way to do this in prod
            # Preferably something with a timer
            #os.remove(file_path)

            found_urls = find_referenced_urls(text_content)
            url_health = Crawler(found_urls).run()

            return jsonify({
            'message': 'File uploaded successfully',
            'file_name': file.filename,
            'text_blocks': text_blocks,
            'pages_amount': pages,
            'text_content': text_content,
            'stated_equals_actual': stated_number_of_pages,
            'referenced_authors': referenced_authors,
            'found_authors': found_authors,
            'found_urls': url_health
            }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Keep root at bottom
@app.route("/")
def read_root():
    return {"message": "Hello, World!"}
