import requests
import json

# ======================
# CONFIGURATION
# ======================

API_KEY = "YOUR_GEMINI_API_KEY"  # <-- replace this with your actual API key
MODEL = "gemini-embedding-001"

# ======================
# INPUT PHRASES
# ======================

phrases = [
    "Hello world",
    "Generative AI is amazing",
    "Python is fun"
]

# ======================
# MAKE THE REQUEST
# ======================

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:embedContent?key={API_KEY}"

data = {
    "text": phrases
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an error for bad HTTP status
    result = response.json()
    print(json.dumps(result, indent=2))  # Pretty print the output

except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
    print(response.text)

except Exception as e:
    print(f"Other error occurred: {e}")
