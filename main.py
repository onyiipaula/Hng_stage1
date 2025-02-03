from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        num = int(number)
        if num < 0:
            raise HTTPException(status_code=400, detail="Negative numbers are not allowed.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid number format. Please provide a valid integer.")

    # Properties determination
    properties = []
    if is_armstrong_number(num):
        properties.append("armstrong")
    properties.append("even" if num % 2 == 0 else "odd")

    # Get number fact
    fact = "No fact available"
    try:
        response = requests.get(f"http://numbersapi.com/{num}/math", timeout=5)
        response.raise_for_status()  # Raise an error for failed requests (e.g., 404, 500)
        fact = response.text
    except requests.exceptions.RequestException:
        fact = "No fact available"

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect_number(num),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(num)),
        "fun_fact": fact
    }

@app.get("/")
async def root():
    return {"message": "Number Classification API is running"}
