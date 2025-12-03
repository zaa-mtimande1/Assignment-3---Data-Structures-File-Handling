from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from the .env file
# Prints the API key to verify it's loaded correctly
print(os.getenv("GEMINI_API_KEY"))
