import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Global configuration variables
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
