import os

from dotenv import load_dotenv

load_dotenv()


ZVENOAI_API_KEY = os.environ.get("ZVENOAI_API_KEY")

LLM_MODEL = os.environ.get("LLM_MODEL", "openai/gpt-oss-120b:free")
