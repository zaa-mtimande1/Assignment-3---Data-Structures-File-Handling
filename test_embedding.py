import os
import google.generativeai as genai

genai.api_key = "AIzaSyB-2cDJwA--3rnZfpAmGI1PwDJVh9Kx57g"
models = genai.list_models()  # or the correct method to list

print("Available models:")
for m in models:
    print(m)
