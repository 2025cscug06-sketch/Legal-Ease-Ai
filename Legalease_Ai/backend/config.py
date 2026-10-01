import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "LegalEase")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:8501",
)

MODEL_MOCK = os.getenv(
    "MODEL_MOCK",
    "false",
).lower() == "true"