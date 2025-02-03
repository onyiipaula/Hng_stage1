from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
import re

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def validate_input(number: str):
    
    
    if not re.match(r'^[0-9]+$', number):
        raise HTTPException(status_code=400, detail={
            "number": number,
            "error": True,
            "message": "Invalid number format. Please provide a valid positive integer."
        })
    
    num = int(number)
    
    
    if num > 1_000_000:
        raise HTTPException(status_code=400, detail={
            "number": number,
            "error": True,
            "message": "Number is out of acceptable range"
        })
    
    return num

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong_number(n):
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

def is_perfect_number(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

def get_number_fact(number):
    """Retrieve a mathematical fact about the number."""
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math", timeout=3)
        return response.text if response.status_code == 200 else "No fact available"
    except (requests.RequestException, ValueError):
        return "No fact available"

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        
        num = validate_input(number)
        
        
        properties = []
        if is_armstrong_number(num):
            properties.append("armstrong")
        properties.append("even" if num % 2 == 0 else "odd")
        
        # Retrieve fun fact
        fun_fact = get_number_fact(num)
        
        # Construct response
        return {
            "number": num,
            "is_prime": is_prime(num),
            "is_perfect": is_perfect_number(num),
            "properties": properties,
            "digit_sum": sum(int(digit) for digit in str(num)),
            "fun_fact": fun_fact
        }
    
    except HTTPException as he:
        
        raise he

@app.get("/")
async def root():
    return {"message": "Number Classification API is running"}