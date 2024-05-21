'''
---pdf_analysis.py---
Functionality to process and analyse uploaded PDF-files
'''
import fitz
import logging
import re

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

def count_pages(pdf_file):
    pages = 0
    try:
        for _ in pdf_file:
            pages += 1
    except Exception as e:
        logging.error(f'Error counting pages: {str(e)}')
        pages = 0

    return pages

# Categorizes text from pdf based on font name and size.
# Outputs blocks of text.
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

# Compares the amount of pages in the chosen file to the number of pages
# declared in the text itself.
# Outputs a string telling the user the result of this.
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
        author_occurrences = [m.start() for m in re.finditer(re.escape(author), text)]
        if author_occurrences:
            found_authors[author] = author_occurrences
    return found_authors

def find_referenced_urls(text):
    found_urls = []
    search_strings = ("http:", "https:")
    lowtext = text.lower()
    ref_section_start = lowtext.find('references')

    if ref_section_start != -1:
        ref_text = lowtext.partition('references')[2]
        for line in ref_text.splitlines():
            if line.startswith(search_strings):
                newline = line.split()[0]
                found_urls.append(newline)
                
    return found_urls