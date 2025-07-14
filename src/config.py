import os
from dotenv import load_dotenv

# Загружаем переменные из.env файла (для локального запуска)
# В GitHub Actions переменные будут браться из Secrets
load_dotenv()

# Получаем переменные окружения
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверяем, что все переменные заданы
# ВОТ ИСПРАВЛЕННАЯ СТРОКА:
if not all():
    raise ValueError("Ошибка: Одна или несколько переменных окружения не заданы. Проверьте ваши GitHub Secrets (GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID).")

# Идентификатор модели Gemini
MODEL_NAME = "gemini-1.5-flash-latest"
