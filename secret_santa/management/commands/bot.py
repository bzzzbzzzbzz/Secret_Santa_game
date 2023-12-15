from aiogram.types import BotCommand, BotCommandScopeDefault
from django.core.management.base import BaseCommand
from secret_santa.bot_logic.loader import bot, dp
from secret_santa.bot_logic import handlers
import asyncio


async def main():
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        asyncio.run(main())
        # commands = [
        #     BotCommand(
        #         command='start',
        #         description='Начало работы'
        #     ),
        #     BotCommand(
        #         command='help',
        #         description='Помощь'
        #     )
        # ]

        # bot.set_my_commands(commands, BotCommandScopeDefault())
        # dp.start_polling(bot)
