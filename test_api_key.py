from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env
api_key = os.getenv("AIzaSyB-2cDJwA--3rnZfpAmGI1PwDJVh9Kx57g")
print(api_key)  # should print the key correctly
