import os
from dotenv import load_dotenv

# Загружаем переменные из.env файла. Это безопасно для продакшена,
# так как в среде GitHub Actions.env файла не будет, и функция ничего не сделает.
load_dotenv()

# Получаем переменные из окружения
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Добавляем ID администратора для получения уведомлений об ошибках
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

# Словарь обязательных переменных для проверки
required_variables = {
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
    "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
    "TELEGRAM_ADMIN_CHAT_ID": TELEGRAM_ADMIN_CHAT_ID
}

# Детальная проверка наличия переменных
missing_vars = [name for name, value in required_variables.items() if not value]

if missing_vars:
    raise ValueError(
        f"Ошибка конфигурации: Отсутствуют следующие обязательные переменные окружения: {', '.join(missing_vars)}. "
        "Проверьте ваш файл.env для локального запуска или настройки Secrets в репозитории GitHub для Actions."
    )

# Конфигурация модели
MODEL_NAME = "gemini-1.5-pro-latest" # Обновлено до последней стабильной модели