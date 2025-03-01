import os
from dotenv import load_dotenv

load_dotenv()

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is set
if not OPENAI_API_KEY:
    raise ValueError("API key is not set! Please set the OPENAI_API_KEY environment variable.")

print("DEBUG: OPENAI_API_KEY =", OPENAI_API_KEY)
