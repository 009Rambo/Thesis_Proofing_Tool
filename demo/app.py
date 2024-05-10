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

        pages = count_pages(file_path)

        stated_number_of_pages = compare_pages(text, pages)


        return jsonify({
            'message': 'File uploaded successfully',
            'file_name': file.filename,
            'file_path': file_path,
            'text_content': text,
            'pages_amount' : pages,
            'stated_equals_actual' : stated_number_of_pages

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


# Here we count the amount of pages in the file
def count_pages(file_path):
    pages = 0
    try:
        with fitz.open(file_path) as pdf_file:
            for page in pdf_file:
                pages += 1
    except Exception as e:
        print( f'Error extracting text: {str(e)}')
    return pages



# Here we compare amount of pages counted on the file to  page amount that is stated on thesis
def compare_pages(text, pages):
    result = ''
    pagesEng = pages

# Extract the number of appendix pages and subtract from the total pages count
# Next lines finds the amount of appendices stated on text and that amount is substracted from the total pages for English format
# These lines should just pass on Finnish format since amount of pages includes appendices 
    appendices_index = text.find("appendices")
    if appendices_index != -1:
        appendices_end_index = text.find("pages", appendices_index)
        appendices_text = text[appendices_index + len("appendices") : appendices_end_index].strip()
        try:
            appendices = int(appendices_text)
            pagesEng -= appendices
        except ValueError:
            pass  # Ignore if the extraction of appendix pages fails

    # Here we try to find the amount of pages stated on file and if the amount is correct and presented in correct format this should return message telling just that.
    index_fi = text.find("Opinnäytetyö " + str(pages) + " sivua")
    index_eng = text.find("thesis " + str(pagesEng) + " pages")

    if index_fi != -1 or index_eng != -1:
        result = 'Amount of pages stated in thesis matches the actual amout ✅'
    else:
        result = '❌❌❌Amount of pages stated in thesis does not match the actual amout ❌❌❌'\
        '\n Make sure you state the amount of pages in one of these formats '\
        '"Opinnäytetyö 55 sivua, joista liitteitä 3 sivua", "Master’s thesis 65 pages, appendices 10 pages" or "Bachelor’s thesis 41 pages, appendices 10 pages".'\
        '\n Notice that on Finnish format the amount of pages includes appendices and on English format pages does not include appenidices.'
    return result





if __name__ == '__main__':
    app.run(debug=True)
