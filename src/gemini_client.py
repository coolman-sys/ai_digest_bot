import logging
import google.generativeai as genai
from google.api_core import exceptions

from src.config import GEMINI_API_KEY, MODEL_NAME

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def configure_gemini():
    """Настраивает API-ключ Gemini."""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("API-ключ Gemini успешно сконфигурирован.")
    except Exception as e:
        logger.error(f"Не удалось сконфигурировать Gemini: {e}")
        raise

def generate_digest(prompt_text: str) -> tuple[str | None, str | None]:
    """
    Генерирует дайджест с помощью модели Gemini.

    Возвращает кортеж (текст_дайджеста, причина_ошибки).
    В случае успеха причина_ошибки будет None.
    """
    try:
        logger.info(f"Запрос к модели {MODEL_NAME}...")
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Устанавливаем настройки безопасности, чтобы получать больше информации
        generation_config = genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0.7, # Немного креативности
        )
        
        response = model.generate_content(
            prompt_text,
            generation_config=generation_config,
        )
        
        logger.info("Ответ от Gemini получен.")

        # Проверяем, есть ли текст в ответе
        if response.text:
            return response.text, None
        
        # Если текста нет, ищем причину в prompt_feedback
        else:
            block_reason = "Причина неизвестна"
            if response.prompt_feedback:
                block_reason = f"Ответ заблокирован. Причина: {response.prompt_feedback.block_reason.name}"
            
            logger.warning(f"Модель Gemini вернула пустой ответ. {block_reason}")
            return None, block_reason

    except exceptions.GoogleAPICallError as e:
        error_message = f"Ошибка вызова API Google: {e}"
        logger.error(error_message)
        return None, error_message
    except Exception as e:
        error_message = f"Непредвиденная ошибка при генерации текста: {e}"
        logger.error(error_message)
        return None, error_message