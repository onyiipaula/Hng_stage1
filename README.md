Number Classification API
Overview
This FastAPI-based microservice provides detailed mathematical classifications for input numbers.
Features

Determine prime numbers
Identify Armstrong numbers
Calculate digit sum
Retrieve mathematical fun facts
Full CORS support

Installation

Clone the repository
Create a virtual environment
Install dependencies:
Copypip install -r requirements.txt


Running the API
bashCopyuvicorn main:app --reload
Endpoint
GET /api/classify-number?number=371
Response Example
jsonCopy{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number"
}
Technologies

FastAPI
Python
Requests Library
Numbers API

Deployment
Can be deployed on platforms like Heroku, Railway, or DigitalOcean