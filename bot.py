import asyncio
import logging
import sys
from http.client import responses
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from checkwords import checkWords

# Bot token can be obtained via https://t.me/BotFather
TOKEN = ("7427403048:AAHZKp_aKhD4e4c0BQrjM8MjpMLQ6HwlXO4")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("help"))  # Yangi help handleri
async def command_help_handler(message: Message) -> None:
    """ /help buyrug'ini qabul qilish uchun handler """
    await message.answer("Botdan foydalanish uchun matn yuboring!\nMisollar:\n- /start\n- /help")


@dp.message()
async def checkImlo(message: Message) -> None:
    word = message.text
    result = checkWords(word)
    if result["available"]:
        response = f"✅ {word.capitalize()}"
    else:
        response = f"❌ {word.capitalize()}\n"
        for text in result['matches']:
            response += f"✅ {text.capitalize()}\n"
    await message.answer(response)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
