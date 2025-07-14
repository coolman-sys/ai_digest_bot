import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ЭТА СТРОКА ТЕПЕРЬ ПОЛНОСТЬЮ ИСПРАВЛЕНА.
# Мы создаем список из реальных переменных для проверки.
variables_to_check =

if not all(variables_to_check):
    raise ValueError("Ошибка: Одна или несколько переменных окружения не заданы. Проверьте ваши GitHub Secrets.")

MODEL_NAME = "gemini-2.5-pro"