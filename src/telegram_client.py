import logging
import telegram
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для Telegram MarkdownV2."""
    escape_chars = r'_*()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

async def send_message(text: str):
    """
    Асинхронно отправляет отформатированное сообщение в Telegram.
    """
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        logging.info(f"Отправка сообщения в чат {TELEGRAM_CHAT_ID}...")
        
        # Экранируем текст перед отправкой
        escaped_text = escape_markdown_v2(text)
        
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=escaped_text,
            parse_mode='MarkdownV2'
        )
        logging.info("Сообщение в Telegram отправлено успешно.")
    except telegram.error.TelegramError as e:
        logging.error(f"Ошибка отправки сообщения в Telegram: {e}")
    except Exception as e:
        logging.error(f"Непредвиденная ошибка при работе с Telegram: {e}")
