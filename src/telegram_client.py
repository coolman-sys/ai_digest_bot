import logging
import telegram
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Лимит Telegram на длину сообщения. Устанавливаем с запасом.
TELEGRAM_MAX_MESSAGE_LENGTH = 4096

async def send_message(text: str, chat_id: str = TELEGRAM_CHAT_ID):
    """
    Отправляет текстовое сообщение в Telegram.
    Если текст превышает лимит, он автоматически разбивается на несколько сообщений.
    """
    if not text:
        logging.warning("Попытка отправить пустое сообщение. Отправка отменена.")
        return

    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        
        if len(text) <= TELEGRAM_MAX_MESSAGE_LENGTH:
            logging.info(f"Отправка цельного сообщения в чат {chat_id}...")
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode='Markdown'
            )
        else:
            logging.info(f"Сообщение превышает лимит ({len(text)} символов). Разбиение на части...")
            parts =
            current_part = ""
            # Разбиваем по строкам, чтобы не рвать Markdown-форматирование
            lines = text.split('\n')
            for line in lines:
                if len(current_part) + len(line) + 1 > TELEGRAM_MAX_MESSAGE_LENGTH:
                    parts.append(current_part)
                    current_part = line
                else:
                    if current_part:
                        current_part += "\n" + line
                    else:
                        current_part = line
            parts.append(current_part) # Добавляем последнюю часть

            logging.info(f"Сообщение разбито на {len(parts)} частей.")
            for i, part in enumerate(parts):
                part_header = f"Дайджест (часть {i + 1}/{len(parts)})\n\n"
                # Проверяем, не превысит ли часть с заголовком лимит
                if len(part_header) + len(part) > TELEGRAM_MAX_MESSAGE_LENGTH:
                     await bot.send_message(
                        chat_id=chat_id,
                        text=part,
                        parse_mode='Markdown'
                    )
                else:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=part_header + part,
                        parse_mode='Markdown'
                    )
                
                logging.info(f"Часть {i + 1} отправлена в чат {chat_id}.")

        logging.info("Сообщение в Telegram отправлено успешно.")
    except telegram.error.TelegramError as e:
        logging.error(f"Ошибка отправки сообщения в Telegram: {e}")
        raise # Передаем исключение наверх для обработки в main
    except Exception as e:
        logging.error(f"Непредвиденная ошибка при работе с Telegram: {e}")
        raise # Передаем исключение наверх для обработки в main