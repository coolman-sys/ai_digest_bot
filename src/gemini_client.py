import logging
import time
import google.generativeai as genai
from google.api_core import exceptions
from src.config import GEMINI_API_KEY, MODEL_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_gemini():
    """Конфигурирует API-ключ Gemini. Вызывает исключение при ошибке."""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logging.info("API-ключ Gemini успешно сконфигурирован.")
    except Exception as e:
        logging.error(f"Не удалось сконфигурировать Gemini: {e}")
        raise # Передаем исключение наверх для обработки в main

def generate_digest(prompt_text: str, max_retries: int = 3, initial_delay: int = 2) -> str | None:
    """
    Генерирует текст с помощью модели Gemini, используя механизм повторных попыток
    с экспоненциальной задержкой.
    """
    retries = 0
    delay = initial_delay
    
    while retries < max_retries:
        try:
            logging.info(f"Запрос к модели {MODEL_NAME} (Попытка {retries + 1}/{max_retries})...")
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt_text)
            logging.info("Ответ от Gemini получен успешно.")
            # Добавлена проверка на пустой ответ или отсутствие текста
            if response.text:
                return response.text
            else:
                logging.warning("Gemini API вернул ответ без текстового содержимого.")
                # Это не ошибка сети, а проблема с контентом, повторять нет смысла
                return None 
        except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable, exceptions.InternalServerError) as e:
            logging.warning(f"Ошибка API Google, допускающая повторную попытку: {e}. Повтор через {delay} сек.")
            retries += 1
            if retries < max_retries:
                time.sleep(delay)
                delay *= 2  # Экспоненциальная задержка
            else:
                logging.error("Превышено максимальное количество попыток обращения к Gemini API.")
                return None
        except exceptions.GoogleAPICallError as e:
            logging.error(f"Критическая ошибка вызова API Google (повтор невозможен): {e}")
            return None
        except Exception as e:
            logging.error(f"Непредвиденная ошибка при генерации текста: {e}")
            return None
    
    return None