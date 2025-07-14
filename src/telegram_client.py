import logging
import telegram
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ADMIN_CHAT_ID

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# A constant for Telegram's max message length
MAX_MESSAGE_LENGTH = 4096

async def send_message(text: str, chat_id: str = TELEGRAM_CHAT_ID):
    """
    Sends a message to a specified Telegram chat.
    If the message is too long, it splits it into multiple parts.
    """
    if not text:
        logger.warning("Attempted to send an empty message. Aborting.")
        return

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    
    if len(text) <= MAX_MESSAGE_LENGTH:
        # If the message is short enough, send it in one go
        try:
            logger.info(f"Sending message to chat_id: {chat_id}")
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode='Markdown'
            )
            logger.info("Message sent successfully.")
        except telegram.error.TelegramError as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")
    else:
        # If the message is too long, split it
        logger.info(f"Message is too long ({len(text)} chars). Splitting into parts.")
        parts = []
        while len(text) > 0:
            if len(text) > MAX_MESSAGE_LENGTH:
                part = text[:MAX_MESSAGE_LENGTH]
                # Find the last newline character to avoid cutting mid-sentence
                last_newline = part.rfind('\n')
                if last_newline != -1:
                    parts.append(part[:last_newline])
                    text = text[last_newline:]
                else:
                    # If no newline, just cut at the max length
                    parts.append(part)
                    text = text[MAX_MESSAGE_LENGTH:]
            else:
                parts.append(text)
                break
        
        for i, part in enumerate(parts):
            try:
                logger.info(f"Sending part {i+1}/{len(parts)} to {chat_id}")
                await bot.send_message(
                    chat_id=chat_id,
                    text=part,
                    parse_mode='Markdown'
                )
            except telegram.error.TelegramError as e:
                logger.error(f"Failed to send part {i+1} to {chat_id}: {e}")

async def send_admin_notification(text: str):
    """Sends a notification message to the admin."""
    logger.info("Sending notification to admin.")
    await send_message(text=text, chat_id=TELEGRAM_ADMIN_CHAT_ID)