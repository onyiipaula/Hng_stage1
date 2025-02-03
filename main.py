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

@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        num = int(number)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid number format. Please provide an integer.")

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
        "is_perfect": num == sum(i for i in range(1, num) if num % i == 0),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(num)),
        "fun_fact": fact
    }

@app.get("/")
async def root():
    return {"message": "Number Classification API is running"}