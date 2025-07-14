import os
from dotenv import load_dotenv

# Загружаем переменные из.env файла (для локального запуска)
# В GitHub Actions переменные будут браться из Secrets
load_dotenv()

# Получаем переменные окружения
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Список переменных для проверки
variables_to_check =

# Правильная проверка, что все переменные заданы
if not all(variables_to_check):
    raise ValueError("Ошибка: Одна или несколько переменных окружения не заданы. Проверьте ваши GitHub Secrets.")

# Правильная модель, которую вы запрашивали
MODEL_NAME = "gemini-2.5-pro"