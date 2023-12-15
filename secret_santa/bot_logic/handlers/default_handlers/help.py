from secret_santa.bot_logic.loader import dp
from aiogram import types
from aiogram.filters.command import Command


@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer("<b>Сервис для обмена новогодними подарками.</b>\n"
                         "\n- Для запуска новой игры введите команду <u>/start</u>\n"
                         "\n- Для участия в игре получите ссылку-приглашение для регистрации в игре")