from secret_santa.bot_logic.loader import dp, bot
from secret_santa.bot_logic.set_bot_commands import set_commands
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await set_commands(bot)
    text = message.text.split()
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEK9qFlevsInA68q_W-0N39iF5-5CCrjwACeAEAAiI3jgQ6pl0vZ69f1TME')
    if len(text) > 1:
        id_organizer = text[1]
        # Запрос на информацию об игре
        await message.answer(f"Замечательно, ты собираешься участвовать в игре: {id_organizer}")
                             # "(вывести на экран данные об игре: название, ограничение стоимости подарка, "
                             # "период регистрации и дата отправки подарков)")
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="Создать игру", callback_data="Создать игру")
        )
        await message.answer("Организуй тайный обмен подарками, 🎄🎄🎄\n"
                             "🎄🎄🎄 запусти праздничное настроение!",
                             reply_markup=builder.as_markup())
    # referral_link = f"https://t.me/Secret_Santa_educational_bot?start={id_user}"
    # print(referral_link)
    # await message.answer("Организуй тайный обмен подарками, запусти праздничное настроение!")
