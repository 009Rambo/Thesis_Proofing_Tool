from typing import Union
from fastapi import FastAPI, File, UploadFile
from typing import List
import fitz
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/check-grammar")
async def check_grammar(file: UploadFile = File(...)):
    # Save the uploaded PDF file
    with open('temp.pdf', 'wb') as f:
        f.write(await file.read())

    # Extract text from PDF
    text = ''
    doc = fitz.open('temp.pdf')
    for page in doc:
        text += page.get_text()

    # Clean up
    doc.close()

    # Check grammar with LanguageTool
    return check_grammar_with_languagetool(text)

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

    # Format results
    grammar_errors = []
    if 'matches' in results:
        for match in results['matches']:
            grammar_errors.append({
                'message': match['message'],
                'context': match['context']['text'],
                'suggested_correction': match['replacements'][0]['value']
            })

    return grammar_errors

