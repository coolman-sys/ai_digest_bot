import asyncio
import logging
# V-- ШАГ 1: УБЕДИТЕСЬ, ЧТО ЭТОТ ИМПОРТ ЕСТЬ --V
from datetime import datetime
import pytz
from src.gemini_client import configure_gemini, generate_digest
from src.telegram_client import send_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news_from_sources() -> str:
    logging.info("Получение новостей из источников (используется заглушка)...")
    mock_news = """
    Новость 1: Google выпустила модель Gemini 2.5 Pro, которая показывает невероятные результаты в решении математических задач.
    Ссылка: https://blog.google/technology/ai/google-gemini-update-flash-2-5-pro/
    
    Новость 2: Стартап Cognition AI представил Devin, первого в мире полностью автономного AI-инженера, способного выполнять сложные проекты.
    Ссылка: https://www.cognition-labs.com/blog/introducing-devin
    """
    return mock_news

def read_prompt_template() -> str:
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Файл prompt.md не найден!")
        raise

async def main():
    logging.info("Запуск бота ai_digest_bot...")
    try:
        configure_gemini()
        news_context = get_news_from_sources()
        prompt_template = read_prompt_template()
        
        # Определяем московский часовой пояс
        moscow_tz = pytz.timezone("Europe/Moscow")
        # Получаем текущую дату и форматируем ее
        current_date = datetime.now(moscow_tz).strftime("%d.%m.%Y")
        
        # V-- ШАГ 2: УБЕДИТЕСЬ, ЧТО СТРОКА НИЖЕ ВЫГЛЯДИТ ИМЕННО ТАК --V
        # Мы передаем в шаблон и новости, и дату
        final_prompt = prompt_template.format(news_context=news_context, current_date=current_date)
        
        digest_text = generate_digest(final_prompt)
        if digest_text:
            await send_message(digest_text)
        else:
            logging.error("Не удалось сгенерировать дайджест. Отправка в Telegram отменена.")
    except Exception as e:
        logging.critical(f"В процессе работы бота произошла критическая ошибка: {e}")
    
    logging.info("Работа бота завершена.")

if __name__ == "__main__":
    asyncio.run(main())