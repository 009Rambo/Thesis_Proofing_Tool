import fitz  # PyMuPDF
import requests

def extract_text_from_pdf(pdf_url):
    # Download PDF file
    response = requests.get(pdf_url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
    
    # Extract text from PDF
    text = ''
    doc = fitz.open('temp.pdf')
    for page in doc:
        text += page.get_text()
    
    # Clean up and return text
    doc.close()
    return text

def check_grammar_with_languagetool(text):
    # LanguageTool API URL
    api_url = 'https://languagetool.org/api/v2/check'
    
    # Request parameters
    params = {
        'text': text,
        'language': 'en-US',  # Set language (e.g., English US)
    }
    
    # Send POST request to LanguageTool API
    response = requests.post(api_url, data=params)
    
    # Parse JSON response
    results = response.json()
    
    # Print grammar suggestions
    if 'matches' in results:
        for match in results['matches']:
            print(f"Message: {match['message']}")
            print(f"Context: {match['context']['text']}")
            print(f"Suggested Correction: {match['replacements'][0]['value']}")
            print("=" * 50)

# Example usage
if __name__ == '__main__':
    pdf_url = 'https://pdfobject.com/pdf/sample.pdf'  # URL of the PDF file
    pdf_text = extract_text_from_pdf(pdf_url)
    check_grammar_with_languagetool(pdf_text)
