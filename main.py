import asyncio
import logging
from src.gemini_client import configure_gemini, generate_digest
from src.telegram_client import send_message

# Настройка логирования для вывода информативных сообщений
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news_from_sources() -> str:
    """
    Получает новости из различных источников.
   !!! ЗАГЛУШКА: В будущем здесь будет код для парсинга новостных сайтов.
    """
    logging.info("Получение новостей из источников (используется заглушка)...")
    # Это пример. В реальном проекте вы будете получать данные с сайтов.
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
        logging.error("Файл prompt.md не найден!")
        raise

async def main():
    """Основная асинхронная функция для запуска бота."""
    logging.info("Запуск бота ai_digest_bot...")
    
    try:
        # 1. Настраиваем API Gemini
        configure_gemini()

        # 2. Получаем новости (пока что из заглушки)
        news_context = get_news_from_sources()

        # 3. Читаем и форматируем промпт
        prompt_template = read_prompt_template()
        final_prompt = prompt_template.format(news_context=news_context)

        # 4. Генерируем дайджест
        digest_text = generate_digest(final_prompt)

        # 5. Если дайджест успешно создан, отправляем его в Telegram
        if digest_text:
            await send_message(digest_text)
        else:
            logging.error("Не удалось сгенерировать дайджест. Отправка в Telegram отменена.")

    except Exception as e:
        logging.critical(f"В процессе работы бота произошла критическая ошибка: {e}")

    logging.info("Работа бота завершена.")


if __name__ == "__main__":
    # Эта конструкция правильно запускает асинхронный код
    # и решает проблему "молчаливого" завершения скрипта.
    asyncio.run(main())
