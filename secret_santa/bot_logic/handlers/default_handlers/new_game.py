import datetime
from aiogram.filters.callback_data import CallbackData
from secret_santa.bot_logic.loader import dp, bot
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from secret_santa.bot_logic.statesform import StepsForm
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from secret_santa.models import Game, Givers

from asgiref.sync import sync_to_async, async_to_sync
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from secret_santa.gifting import perform_pairing
# from default_handlers.start import perform_pairing

NAME_GAME = None
PRICE = None
END_OF_REGISTRATION = None


@dp.callback_query(F.data == "Создать игру")
async def new_game(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название игры")
    await state.set_state(StepsForm.NAME_OF_THE_GAME)


@dp.message(StepsForm.NAME_OF_THE_GAME)
async def name_of_game(message: types.Message, state: FSMContext):
    await state.clear()
    global NAME_GAME
    NAME_GAME = message.text
    if len(NAME_GAME) > 25:
        difference = len(NAME_GAME) - 25
        await message.answer(f"максимальное колличество символов в названии 25, "
                             f"Вам необходимо сократить Ваше название на {difference} символов")
        await message.answer("Введите название игры")
        await state.set_state(StepsForm.NAME_OF_THE_GAME)
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="Да", callback_data="Ограничение")
        )
        builder.row(types.InlineKeyboardButton(
            text="Нет", callback_data="Без ограничений")
        )
        await message.answer("Ограничение стоимости подарка:",
                             reply_markup=builder.as_markup())


@dp.callback_query(F.data == "Ограничение")
async def gift_price(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="до 500 рублей", callback_data="500 рублей")
    )
    builder.add(types.InlineKeyboardButton(
        text="500-1000 рублей", callback_data="500-1000 рублей")
    )
    builder.row(types.InlineKeyboardButton(
        text="1000-2000 рублей", callback_data="1000-2000 рублей")
    )
    builder.add(types.InlineKeyboardButton(
        text="Без ограничений", callback_data="Без ограничений")
    )
    await callback.message.answer("Выберите ограничение стоимости подарка:",
                                  reply_markup=builder.as_markup())


@dp.callback_query(F.data.in_(["Без ограничений", "500 рублей", "500-1000 рублей", "1000-2000 рублей"]))
async def registration_period(callback: types.CallbackQuery):
    if callback.data in ("500 рублей", "500-1000 рублей", "1000-2000 рублей"):
        global PRICE
        PRICE = callback.data
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="до 25.12.2023", callback_data="25")
    )
    builder.add(types.InlineKeyboardButton(
        text="до 31.12.2023", callback_data="31")
    )
    await callback.message.answer("Период регистрации участников:",
                                  reply_markup=builder.as_markup())


@dp.callback_query(F.data.in_(["31", "25"]))
async def date_the_gift_was_sent(callback: types.CallbackQuery):
    global END_OF_REGISTRATION
    END_OF_REGISTRATION = f"{callback.data}.12.2023"
    await callback.message.answer("Дата отправки подарка:",
                                  reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar()
    calendar.set_dates_range(datetime.datetime(2022, 1, 1), datetime.datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        global PRICE
        if not PRICE:
            PRICE = "любая сумма"
        user_id = callback_query.from_user.id
        data = str(END_OF_REGISTRATION).split('.')
        end_of_registration = datetime.date(int(data[2]), int(data[1]), int(data[0]))
        data_now = f"{datetime.date.today().day}.{datetime.date.today().month}.{datetime.date.today().year}"
        departure_date = date.strftime("%d.%m.%Y")
        data2 = date.strftime("%Y.%m.%d").split('.')
        departure_date2 = datetime.date(int(data2[0]), int(data2[1]), int(data2[2]))
        # link = f"https://t.me/Secret_Santa_educational_bot?start={callback_query.from_user.id}"
        link = f"https://t.me/sec_santa_test_bot?start={callback_query.from_user.id}"
        # Game.objects.create(name_of_game=NAME_GAME, creators_id=user_id, cost_of_the_gift=PRICE,
        #                     start_of_registration=datetime.date.today(), end_of_registration=end_of_registration,
        #                     departure_date=departure_date2)
        new_game = Game(name_of_game=NAME_GAME, creators_id=user_id, cost_of_the_gift=PRICE,
                        start_of_registration=datetime.date.today(), end_of_registration=end_of_registration,
                        departure_date=departure_date2, link_to_the_game=link)
        await sync_to_async(new_game.save)()
        await callback_query.message.answer(f"Отлично, Тайный Санта уже готовится к раздаче подарков!\n"
                                            f"\n<b>Ссылка на игру для регистрации участников</b> - {link}\n"
                                            f"\n<u>Название игры</u> - \"{NAME_GAME}\"\n"
                                            f"<u>Цена подарка</u> - {PRICE}\n"
                                            f"<u>Период регистрации</u> с {data_now} по {END_OF_REGISTRATION}\n"
                                            f"<u>Дата отправки подарка</u> - {departure_date}")

        schebuler = AsyncIOScheduler()
        schebuler.add_job(announce, trigger="date",
                          next_run_time=datetime.datetime.strptime( END_OF_REGISTRATION, '%d.%m.%Y' ),
                          # next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=60),
                          kwargs={'games': [new_game]})
        schebuler.start()

        await bot.send_sticker(callback_query.from_user.id,
                               sticker='CAACAgIAAxkBAAEK9qZlev4Je4A1JHcJBja16ILaYfhR5gAC1QUAAj-VzAr0FV2u85b8KDME')


async def announce(games):
    for game in games:
        gifters = await sync_to_async(perform_pairing)([game])
        for pair in gifters:
            await bot.send_message(pair.givers.id_user, pair.message)
