import os
from dotenv import load_dotenv

# Загружаем переменные из.env файла
load_dotenv()

# Получаем переменные окружения
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверяем, что все переменные заданы
if not all():
    raise ValueError("Ошибка: Не заданы одна или несколько переменных окружения (GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)")

# Идентификатор модели Gemini
MODEL_NAME = "gemini-1.5-flash-latest" # Используем более быструю и дешевую модель для дайджестов
