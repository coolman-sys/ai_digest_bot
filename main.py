import asyncio
import logging
from datetime import datetime
import pytz

from src.gemini_client import configure_gemini, generate_digest
from src.telegram_client import send_message, send_admin_notification
from src.news_fetcher import fetch_news # Предполагаем, что этот модуль будет создан

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_news_from_sources() -> str:
    """
    Получает новости из различных источников.
    !!! ВРЕМЕННАЯ ЗАГЛУШКА !!!
    """
    logger.info("Получение новостей из источников (используется заглушка)...")
    # В будущем здесь будет вызов функции из news_fetcher
    mock_news = """
    Новость 1: Google выпустила модель Gemini 2.5 Pro, которая показывает невероятные результаты в решении математических задач.
    Ссылка: https://blog.google/technology/ai/google-gemini-update-flash-2-5-pro/
    
    Новость 2: Стартап Cognition AI представил Devin, первого в мире полностью автономного AI-инженера, способного выполнять сложные проекты.
    Ссылка: https://www.cognition-labs.com/blog/introducing-devin
    """
    return mock_news

def read_prompt_template() -> str:
    """Читает шаблон промпта из файла."""
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Файл prompt.md не найден!")
        raise

async def main():
    """Основная асинхронная функция для запуска бота."""
    logger.info("Запуск бота ai_digest_bot...")
    try:
        configure_gemini()
        news_context = get_news_from_sources()
        prompt_template = read_prompt_template()
        
        moscow_tz = pytz.timezone("Europe/Moscow")
        current_date = datetime.now(moscow_tz).strftime("%d.%m.%Y")
        
        final_prompt = prompt_template.format(news_context=news_context, current_date=current_date)
        
        digest_text, error_reason = generate_digest(final_prompt)
        
        if digest_text:
            await send_message(digest_text)
        else:
            # Если дайджест не сгенерирован, отправляем уведомление администратору
            error_message_for_admin = (
                "🔴 **Критическая ошибка в ai_digest_bot** 🔴\n\n"
                "Не удалось сгенерировать дайджест.\n\n"
                f"**Причина:** {error_reason or 'Неизвестная ошибка'}"
            )
            logger.error("Не удалось сгенерировать дайджест. Отправка уведомления администратору...")
            await send_admin_notification(error_message_for_admin)

    except Exception as e:
        critical_error_message = (
            "🆘 **Полный отказ системы ai_digest_bot** 🆘\n\n"
            f"Произошла непредвиденная ошибка на самом верхнем уровне: {e}\n\n"
            "Требуется немедленное вмешательство!"
        )
        logger.critical(f"В процессе работы бота произошла критическая ошибка: {e}")
        try:
            await send_admin_notification(critical_error_message)
        except Exception as admin_e:
            logger.error(f"Не удалось даже отправить уведомление администратору: {admin_e}")
    
    logger.info("Работа бота завершена.")

if __name__ == "__main__":
    asyncio.run(main())