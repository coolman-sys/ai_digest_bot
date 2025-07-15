import logging
import telegram
import re
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ADMIN_CHAT_ID

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# A constant for Telegram's max message length
MAX_MESSAGE_LENGTH = 4096

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для Telegram MarkdownV2."""
    # Список символов для экранирования в MarkdownV2
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

async def send_message(text: str, chat_id: str = TELEGRAM_CHAT_ID):
    """
    Sends a message to a specified Telegram chat.
    If the message is too long, it splits it into multiple parts.
    Escapes MarkdownV2 characters to prevent parsing errors.
    """
    if not text:
        logger.warning("Attempted to send an empty message. Aborting.")
        return

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    
    if len(text) <= MAX_MESSAGE_LENGTH:
        try:
            logger.info(f"Sending message to chat_id: {chat_id}")
            safe_text = escape_markdown_v2(text)
            await bot.send_message(
                chat_id=chat_id,
                text=safe_text,
                parse_mode='MarkdownV2'
            )
            logger.info("Message sent successfully.")
        except telegram.error.TelegramError as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")
    else:
        logger.info(f"Message is too long ({len(text)} chars). Splitting into parts.")
        parts = []
        while len(text) > 0:
            if len(text) > MAX_MESSAGE_LENGTH:
                part = text[:MAX_MESSAGE_LENGTH]
                last_newline = part.rfind('\n')
                if last_newline != -1:
                    parts.append(part[:last_newline])
                    text = text[last_newline:]
                else:
                    parts.append(part)
                    text = text[MAX_MESSAGE_LENGTH:]
            else:
                parts.append(text)
                break
        
        for i, part in enumerate(parts):
            try:
                logger.info(f"Sending part {i+1}/{len(parts)} to {chat_id}")
                safe_part = escape_markdown_v2(part)
                await bot.send_message(
                    chat_id=chat_id,
                    text=safe_part,
                    parse_mode='MarkdownV2'
                )
            except telegram.error.TelegramError as e:
                logger.error(f"Failed to send part {i+1} to {chat_id}: {e}")

async def send_admin_notification(text: str):
    """Sends a notification message to the admin."""
    logger.info("Sending notification to admin.")
    await send_message(text=text, chat_id=TELEGRAM_ADMIN_CHAT_ID)