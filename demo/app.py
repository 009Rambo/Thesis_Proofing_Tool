from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF for PDF processing
import logging
import re

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

        # Process the uploaded file in memory
        pdf_file = fitz.open(stream=file.read(), filetype="pdf")

        # Extract text content and analyze PDF
        text_content, text_blocks, pages = process_pdf(pdf_file)

        # Extract referenced author names from the reference list
        referenced_authors = extract_referenced_authors(text_content)

        # Search for referenced author names in the actual text
        found_authors = search_referenced_authors_in_text(text_content, referenced_authors)

        # Count pages and compare with stated number of pages
        stated_number_of_pages = compare_pages(text_content, pages)

        return jsonify({
            'message': 'File uploaded successfully',
            'file_name': file.filename,
            'text_blocks': text_blocks,
            'pages_amount': pages,
            'text_content': text_content,
            'stated_equals_actual': stated_number_of_pages,
            'referenced_authors': referenced_authors,
            'found_authors': found_authors
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_pdf(pdf_file):
    text_content = extract_text_from_pdf(pdf_file)
    text_blocks = analyze_pdf(pdf_file)
    pages = count_pages(pdf_file)
    return text_content, text_blocks, pages

def extract_text_from_pdf(pdf_file):
    text = ''
    try:
        for page in pdf_file:
            page_text = page.get_text()
            if page_text.strip():  # Skip empty pages
                text += page_text
    except Exception as e:
        logging.error(f'Error extracting text: {str(e)}')
        text = ''

    return text

def analyze_pdf(pdf_file):
    text_blocks = {
        'paragraphs': [],
        'headings': [],
        'numbers': [],
        'table_of_contents': []
    }
    try:
        for page in pdf_file:
            page_text = page.get_text()
            if page_text.strip():  # Skip empty pages
                for block in page.get_text("dict")["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            current_text = ""
                            current_font_size = None
                            current_font_name = None

                            for span in line["spans"]:
                                text = span["text"].strip()
                                font_size = span["size"]
                                font_name = span["font"]

                                # Define criteria for paragraphs and headings based on font size
                                if font_size == current_font_size and font_name == current_font_name:
                                    current_text += " " + text  # Append to current text
                                else:
                                    # Create new text block (paragraph or heading)
                                    if current_text:
                                        add_text_block(text_blocks, current_text, current_font_size, current_font_name)

                                    # Reset current text to the new span's text
                                    current_text = text
                                    current_font_size = font_size
                                    current_font_name = font_name

                            # Add the last text block (paragraph or heading) in the line
                            if current_text:
                                add_text_block(text_blocks, current_text, current_font_size, current_font_name)

    except Exception as e:
        logging.error(f'Error analyzing PDF: {str(e)}')
        text_blocks = {'paragraphs': [], 'headings': [], 'numbers': [], 'table_of_contents': []}

    return text_blocks

def add_text_block(text_blocks, text, font_size, font_name):
    text_block = {
        'text': text.strip(),
        'font_size': font_size,
        'font_name': font_name
    }
    if font_size > 12:
        text_blocks['headings'].append(text_block)
    elif text.isdigit():  # Check if the text is a number
        text_blocks['numbers'].append(text_block)
    elif 'contents' in text.lower():  # Check if the text is part of the table of contents
        text_blocks['table_of_contents'].append(text_block)
    else:
        text_blocks['paragraphs'].append(text_block)

def count_pages(pdf_file):
    pages = 0
    try:
        for _ in pdf_file:
            pages += 1
    except Exception as e:
        logging.error(f'Error counting pages: {str(e)}')
        pages = 0

    return pages

def compare_pages(text, pages):
    result = ''
    pagesEng = pages

    # Extract the number of appendix pages and subtract from the total pages count
    # Next lines find the amount of appendices stated in the text
    appendices_index = text.find("appendices")
    if appendices_index != -1:
        appendices_end_index = text.find("pages", appendices_index)
        appendices_text = text[appendices_index + len("appendices") : appendices_end_index].strip()
        try:
            appendices = int(appendices_text)
            pagesEng -= appendices
        except ValueError:
            pass  # Ignore if the extraction of appendix pages fails

    # Here we try to find the amount of pages stated in the file
    index_fi = text.find("Opinnäytetyö " + str(pages) + " sivua")
    index_eng = text.find("thesis " + str(pagesEng) + " pages")

    if index_fi != -1 or index_eng != -1:
        result = 'Amount of pages stated in thesis matches the actual amount ✅'
    else:
        result = '❌❌❌Amount of pages stated in thesis does not match the actual amount ❌❌❌' \
                 '\n Make sure you state the amount of pages in one of these formats ' \
                 '"Opinnäytetyö 55 sivua, joista liitteitä 3 sivua", "Master’s thesis 65 pages, appendices 10 pages" or "Bachelor’s thesis 41 pages, appendices 10 pages".' \
                 '\n Notice that on Finnish format the amount of pages includes appendices and on English format pages does not include appendices.'
    return result

def extract_referenced_authors(text):
    # Regular expression to find author names in reference list
    author_pattern = re.compile(r'\b[A-Z][a-z]*, [A-Z]\b')
    references_section_start = text.find('References')
    if references_section_start == -1:
        references_section_start = text.find('REFERENCES')

    if references_section_start != -1:
        references_section_text = text[references_section_start:]
        authors = author_pattern.findall(references_section_text)
        return list(set(authors))  # Return unique authors
    return []

def search_referenced_authors_in_text(text, authors):
    found_authors = {}
    for author in authors:
        references_section_author = text.find(author)
        #references_section_author = text[references_section_author:]
        author_occurrences = [m.start() for m in re.finditer(re.escape(author), text)]
        if author_occurrences:
            found_authors[author] = author_occurrences
    return found_authors



if __name__ == '__main__':
    app.run()
