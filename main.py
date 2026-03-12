import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Инициализация логгера для отслеживания работы системы
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения. 
# Рекомендуется использовать .env файл в продакшн-среде.
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Инициализация диспетчера
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start. Приветствует пользователя.
    """
    user_name = html.bold(message.from_user.full_name)
    await message.answer(f"Здравствуйте, {user_name}! Я ваш функциональный AI-агент.")
    logger.info(f"User {message.from_user.id} started the bot.")

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Обработчик всех входящих текстовых сообщений (эхо-режим).
    Демонстрирует базовую обработку данных.
    """
    try:
        # Отправляем копию сообщения пользователю
        await message.send_copy(chat_id=message.chat.id)
    except Exception as e:
        logger.error(f"Error while handling message: {e}")
        await message.answer("Произошла ошибка при обработке сообщения.")

async def main() -> None:
    """
    Точка входа: инициализация бота и запуск процесса опроса (polling).
    """
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.critical("BOT_TOKEN не установлен! Пожалуйста, задайте переменную окружения.")
        return

    # Инициализация экземпляра бота с поддержкой HTML разметки
    bot = Bot(
        token=TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Запуск polling (ожидания обновлений от Telegram)
    logger.info("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually.")