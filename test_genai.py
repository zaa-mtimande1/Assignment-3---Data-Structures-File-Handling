# test_genai.py
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.api_key = os.getenv("GENAI_API_KEY")

print("API key loaded:", genai.api_key)
