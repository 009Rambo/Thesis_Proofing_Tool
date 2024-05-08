from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List, Union
import fitz
import requests

app = FastAPI()

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/hello/")
async def read_hello():
    return {"message": "Hello, World!"}

@app.get("/greet/{name}")
async def read_greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "message": "Hello, World!"}



@app.post("/")
async def check_grammar(file: UploadFile = File(...)):
    try:
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
        grammar_errors = await check_grammar_with_languagetool(text)
        return grammar_errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def check_grammar_with_languagetool(text):
    try:
        # LanguageTool API URL
        api_url = 'https://languagetool.org/api/v2/check'

        # Request parameters
        params = {
            'text': text,
            'language': 'en-US',  # Set language (e.g., English US)
        }

        # Send POST request to LanguageTool API
        response = await requests.post(api_url, data=params)
        response.raise_for_status()  # Raise exception for non-200 status codes

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
