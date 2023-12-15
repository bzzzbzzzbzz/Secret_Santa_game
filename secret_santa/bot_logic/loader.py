from django.conf import settings
from aiogram import Bot, Dispatcher

default_commands = (
    ('start', "Запустить бота"),
)

bot_token = settings.TELEGRAM_BOT_API_TOKEN

bot = Bot(bot_token, parse_mode="HTML")
dp = Dispatcher()
