import logging
from datetime import datetime
import pytz

# Убираем 'src.' для более надежного импорта
from gemini_client import configure_gemini, generate_digest
from telegram_client import send_message, send_admin_notification
# Теперь мы ИСПОЛЬЗУЕМ эту функцию
from news_fetcher import fetch_news 

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        
        # --- ИСПРАВЛЕНИЕ №1: Используем настоящую функцию получения новостей ---
        # Удаляем вызов заглушки и вызываем fetch_news
        news_context = fetch_news(limit_per_feed=3) # Берем по 3 новости с каждого ресурса
        
        if "Новостей для анализа не найдено" in news_context:
            logger.warning("Не найдено новостей для обработки. Работа завершена.")
            await send_admin_notification("ℹ️ **Информация о запуске aidigestbot** ℹ️\n\nНе было найдено свежих новостей для обработки. Дайджест не был создан.")
            return

        prompt_template = read_prompt_template()
        
        moscow_tz = pytz.timezone("Europe/Moscow")
        current_date = datetime.now(moscow_tz).strftime("%d.%m.%Y")
        
        final_prompt = prompt_template.format(news_context=news_context, current_date=current_date)
        
        # Логирование финального промпта для отладки
        logger.info("--- Финальный промпт для Gemini ---")
        logger.info(final_prompt)
        logger.info("---------------------------------")
        
        digest_text, error_reason = await generate_digest(final_prompt)
        
        if digest_text:
            await send_message(digest_text)
            logger.info("Дайджест успешно сгенерирован и отправлен.")
        else:
            error_message_for_admin = (
                "🔴 **Критическая ошибка в ai_digest_bot** 🔴\n\n"
                "Не удалось сгенерировать дайджест.\n\n"
                f"**Причина:** {error_reason or 'Неизвестная ошибка от Gemini'}"
            )
            logger.error("Не удалось сгенерировать дайджест. Отправка уведомления администратору...")
            await send_admin_notification(error_message_for_admin)

    except Exception as e:
        critical_error_message = (
            "🆘 **Полный отказ системы aidigest_bot** 🆘\n\n"
            f"Произошла непредвиденная ошибка на самом верхнем уровне: {e}\n\n"
            "Требуется немедленное вмешательство!"
        )
        logger.critical(f"В процессе работы бота произошла критическая ошибка: {e}", exc_info=True)
        try:
            await send_admin_notification(critical_error_message)
        except Exception as admin_e:
            logger.error(f"Не удалось даже отправить уведомление администратору: {admin_e}")
    
    logger.info("Работа бота завершена.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
