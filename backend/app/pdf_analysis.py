'''
---pdf_analysis.py---
Functionality to process and analyse uploaded PDF-files
'''
import fitz

def process_pdf(file_path):
    text_content = extract_text_from_pdf(file_path)
    text_blocks = analyze_pdf(file_path)
    pages = count_pages(file_path)
    return text_content, text_blocks, pages

def extract_text_from_pdf(file_path):
    text = ''
    try:
        with fitz.open(file_path) as pdf_file:
            for page in pdf_file:
                page_text = page.get_text()
                if page_text.strip():  # Skip empty pages
                    text += page_text
    except Exception as e:
        raise RuntimeError(f'Error extracting text: {str(e)}')

    return text

def count_pages(file_path):
    pages = 0
    try:
        with fitz.open(file_path) as pdf_file:
            for _ in pdf_file:
                pages += 1
    except Exception as e:
        raise RuntimeError(f'Error counting pages: {str(e)}')

    return pages

# Categorizes text from pdf based on font name and size.
# Outputs blocks of text.
def analyze_pdf(file_path):
    text_blocks = {
        'paragraphs': [],
        'headings': []
    }
    try:
        with fitz.open(file_path) as pdf_file:
            for page in pdf_file:
                page_text = page.get_text()
                if page_text.strip():  # Skip empty pages
                    for block in page.get_text("dict")["blocks"]:
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
                                        text_block = {
                                            'text': current_text.strip(),
                                            'font_size': current_font_size,
                                            'font_name': current_font_name
                                        }
                                        if current_font_size > 12:
                                            text_blocks['headings'].append(text_block)
                                        else:
                                            text_blocks['paragraphs'].append(text_block)

                                    # Reset current text to the new span's text
                                    current_text = text
                                    current_font_size = font_size
                                    current_font_name = font_name

                            # Add the last text block (paragraph or heading) in the line
                            if current_text:
                                text_block = {
                                    'text': current_text.strip(),
                                    'font_size': current_font_size,
                                    'font_name': current_font_name
                                }
                                if current_font_size > 12:
                                    text_blocks['headings'].append(text_block)
                                else:
                                    text_blocks['paragraphs'].append(text_block)

    except Exception as e:
        raise RuntimeError(f'Error analyzing PDF: {str(e)}')

    return text_blocks

# Compares the amount of pages in the chosen file to the number of pages
# declared in the text itself.
# Outputs a string telling the user the result of this.
def compare_pages(text, pages):
    result = ''
    pagesEng = pages

# Extract the number of appendix pages and subtract from the total pages count
# Next lines finds the amount of appendices stated on text and that amount is 
# substracted from the total pages for English format.
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

    # Here we try to find the amount of pages stated on file and if the amount is correct
    # and presented in correct format this should return message telling just that.
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