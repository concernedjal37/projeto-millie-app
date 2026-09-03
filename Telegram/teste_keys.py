from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
GEMINI_API_HASH = os.getenv("GEMINI_API_HASH")
