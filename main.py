import asyncio
import logging
from datetime import datetime
import pytz
from src.gemini_client import configure_gemini, generate_digest
from src.telegram_client import send_message
from src.config import TELEGRAM_ADMIN_CHAT_ID  # Импортируем ID администратора

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
)

def get_news_from_sources() -> str:
    """
    Получает новостной контент. В текущей версии используется заглушка.
    В будущем здесь будет реализована логика парсинга RSS или API.
    """
    logging.info("Получение новостей из источников (используется заглушка)...")
    # TODO: Заменить эту заглушку на реальную логику получения новостей
    mock_news = """
    Новость 1: Google выпустила модель Gemini 2.5 Pro, которая показывает невероятные результаты в решении математических задач.
    Ссылка: https://blog.google/technology/ai/google-gemini-update-flash-2-5-pro/
    
    Новость 2: Стартап Cognition AI представил Devin, первого в мире полностью автономного AI-инженера, способного выполнять сложные проекты.
    Ссылка: https://www.cognition-labs.com/blog/introducing-devin
    """
    return mock_news

def read_prompt_template() -> str | None:
    """Читает шаблон промпта из файла prompt.md."""
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Критическая ошибка: Файл prompt.md не найден! Работа не может быть продолжена.")
        return None
    except Exception as e:
        logging.error(f"Не удалось прочитать файл prompt.md: {e}")
        return None

async def run_digest_cycle():
    """Основной цикл работы бота: получение, генерация и отправка дайджеста."""
    logging.info("Запуск цикла генерации дайджеста...")
    
    # Шаг 1: Конфигурация API
    try:
        configure_gemini()
    except Exception as e:
        logging.critical(f"Не удалось сконфигурировать Gemini API. Прерывание выполнения. Ошибка: {e}")
        # Отправляем уведомление об ошибке администратору
        await send_message(
            f"КРИТИЧЕСКИЙ СБОЙ: Не удалось сконфигурировать Gemini API. Бот остановлен. Ошибка: {e}",
            chat_id=TELEGRAM_ADMIN_CHAT_ID
        )
        return

    # Шаг 2: Чтение промпта
    prompt_template = read_prompt_template()
    if not prompt_template:
        # Сообщение об ошибке уже залогировано в функции
        await send_message(
            "КРИТИЧЕСКИЙ СБОЙ: Файл prompt.md не найден. Бот остановлен.",
            chat_id=TELEGRAM_ADMIN_CHAT_ID
        )
        return

    # Шаг 3: Получение новостей
    news_context = get_news_from_sources()
    
    # Шаг 4: Формирование финального промпта
    try:
        moscow_tz = pytz.timezone("Europe/Moscow")
        current_date = datetime.now(moscow_tz).strftime("%d.%m.%Y")
        final_prompt = prompt_template.format(news_context=news_context, current_date=current_date)
    except KeyError as e:
        logging.error(f"Ошибка форматирования промпта. Возможно, в шаблоне неверный плейсхолдер: {e}")
        await send_message(
            f"ОШИБКА: Не удалось отформатировать промпт. Плейсхолдер {e} не найден.",
            chat_id=TELEGRAM_ADMIN_CHAT_ID
        )
        return

    # Шаг 5: Генерация дайджеста
    digest_text = None
    try:
        digest_text = generate_digest(final_prompt)
    except Exception as e:
        logging.error(f"Произошла ошибка на этапе генерации дайджеста: {e}")
        await send_message(
            f"ОШИБКА: Сбой при генерации текста моделью Gemini. Ошибка: {e}",
            chat_id=TELEGRAM_ADMIN_CHAT_ID
        )
        return

    # Шаг 6: Отправка дайджеста
    if digest_text:
        try:
            await send_message(digest_text)
        except Exception as e:
            logging.error(f"Произошла ошибка на этапе отправки сообщения в Telegram: {e}")
            await send_message(
                f"ОШИБКА: Дайджест был сгенерирован, но не удалось отправить его в Telegram. Ошибка: {e}",
                chat_id=TELEGRAM_ADMIN_CHAT_ID
            )
    else:
        logging.warning("Не удалось сгенерировать дайджест. Отправка в Telegram отменена.")
        await send_message(
            "ПРЕДУПРЕЖДЕНИЕ: Модель Gemini вернула пустой ответ. Дайджест не был сгенерирован.",
            chat_id=TELEGRAM_ADMIN_CHAT_ID
        )

async def main():
    """Главная точка входа в приложение."""
    logging.info("Запуск бота ai_digest_bot...")
    try:
        await run_digest_cycle()
    except Exception as e:
        logging.critical(f"В процессе работы бота произошла непредвиденная критическая ошибка: {e}")
        try:
            # Последняя попытка уведомить администратора
            await send_message(
                f"КРИТИЧЕСКИЙ СБОЙ УРОВНЯ ПРИЛОЖЕНИЯ: {e}",
                chat_id=TELEGRAM_ADMIN_CHAT_ID
            )
        except Exception as alert_e:
            logging.error(f"Не удалось даже отправить уведомление о сбое: {alert_e}")
    
    logging.info("Работа бота завершена.")

if __name__ == "__main__":
    # Проверка наличия необходимых переменных окружения вынесена в config.py
    # Если их нет, приложение упадет при импорте с понятной ошибкой.
    asyncio.run(main())