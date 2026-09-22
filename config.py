import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-120b"          # <-- changed from llama-3.3-70b-versatile

MAX_STEPS = 20
WORKSPACE_DIR = os.path.abspath("workspace")

if not API_KEY:
    raise RuntimeError("API key missing in .env")