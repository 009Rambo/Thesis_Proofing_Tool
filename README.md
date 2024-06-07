# Thesis_Proofing_Tool
Project for TAMK summer training 2024. 

## Project Description
Thesis Proofing Tool is a Web-based App in which a student working on their Bachelor's or Master's Thesis can submit it to be automatically analyzed for errors and mistakes, according to the standards laid out in the TAMK (Tampere University of Applied Sciences) report guide.
## Technical Description
The frontend was developed using HTML/CSS/JS. No additional external libraries were used in the frontend.  
The backend was developed with Python.  
The following libraries were used:
- Flask 3.0.3
- PyMuPDF 1.24.5
- aiohttp 3.9.5
- Flask-Cors 4.0.1
## How to run locally
First, clone the repository.  
  
To run this app, you will need:
- Node.js
- Python 3.8 or later
- Your favorite CLI

From Node, install [http-server](https://www.npmjs.com/package/http-server):  
`npm i http-server`  
  
Then, in the backend folder, run:  
`pip install -r requirements.txt`  
  
To run the app locally, in the frontend folder:  
`http-server -c-1`  
And in the backend folder:  
`flask --app main.py run --debug`  
(If this doesn't work try adding `python -m` before the `flask`)  
Your frontend should now be running on `localhost:8080`, and your backend on `localhost:5000`.