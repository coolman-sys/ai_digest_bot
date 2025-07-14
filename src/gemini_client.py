import logging
import google.generativeai as genai
from google.api_core import exceptions
from src.config import GEMINI_API_KEY, MODEL_NAME

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_gemini():
    """Настраивает API-ключ для Gemini."""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logging.info("API-ключ Gemini успешно сконфигурирован.")
    except Exception as e:
        logging.error(f"Не удалось сконфигурировать Gemini: {e}")
        raise

def generate_digest(prompt_text: str) -> str | None:
    """
    Генерирует текст дайджеста с помощью модели Gemini.
    Возвращает сгенерированный текст или None в случае ошибки.
    """
    try:
        logging.info(f"Запрос к модели {MODEL_NAME}...")
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt_text)
        logging.info("Ответ от Gemini получен успешно.")
        return response.text
    except exceptions.GoogleAPICallError as e:
        logging.error(f"Ошибка вызова API Google: {e}")
    except Exception as e:
        logging.error(f"Непредвиденная ошибка при генерации текста: {e}")
    
    return None
