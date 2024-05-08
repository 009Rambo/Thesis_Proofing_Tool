from flask import Flask, render_template, request, jsonify
import os
import fitz  # PyMuPDF for PDF processing

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
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

        # Extract text content from the PDF file
        text = extract_text_from_pdf(file_path)

        return jsonify({
            'message': 'File uploaded successfully',
            'file_name': file.filename,
            'file_path': file_path,
            'text_content': text
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_text_from_pdf(file_path):
    text = ''
    try:
        with fitz.open(file_path) as pdf_file:
            for page in pdf_file:
                text += page.get_text()
    except Exception as e:
        text = f'Error extracting text: {str(e)}'
    return text

if __name__ == '__main__':
    app.run(debug=True)
