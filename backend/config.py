from dotenv import load_dotenv
import os


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Optional check
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing! Please set it in your .env file.")
