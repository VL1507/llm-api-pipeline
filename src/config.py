import os

from dotenv import load_dotenv

load_dotenv()


API_KEY = os.environ.get("API_KEY")

BASE_URL = os.environ.get("BASE_URL")

LLM_MODEL = os.environ.get("LLM_MODEL", "openai/gpt-oss-120b:free")
