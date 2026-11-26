import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BASE_URL = os.getenv("BASE_URL", "https://dummypay.vercel.app")

USER_A_EMAIL = os.getenv("USER_A_EMAIL")
USER_A_PASSWORD = os.getenv("USER_A_PASSWORD")

USER_B_EMAIL = os.getenv("USER_B_EMAIL")
USER_B_PASSWORD = os.getenv("USER_B_PASSWORD")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")