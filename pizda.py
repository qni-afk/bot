import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = "7789322601:AAHBQTRFGVBoQARf7Sc4fGad668332wr1l4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список милых сообщений
cute_messages = [
    "Ев, мне безумно нравится с тобой болтать по телефону",
    "Когда я вижу тебе на фотографии и или видео всегда радуюсь",
    "Мне очень с тобой комфортно.",
    "Улыбайся чаще.",
    "Я очень сильно тебя люблю! ❤️",
    "Ты у меня очень красивая!",
    "Ты очень интересная",
    "С тобой я чувствую себя самым счастливым человеком.",
    "Ты очень добрая",
    "Просто хотел сказать, что ты у меня самая лучшая!"
]

# Список фраз из фильмов
movie_quotes = [
    """Дневник памяти (The Notebook, 2004): За мной только что бежали двое полицейских. Я не уверен, что готов на такие
жертвы ради тебя.""",
    """“500 дней лета**” (500 Days of Summer, 2009): “Я люблю ее улыбку. Я люблю ее родинки на шее.Я люблю, как она смеется. Я люблю, как она выглядит, когда спит. Я люблю ее, и,когда она заходит в комнату, я чувствую, как меняется атмосфера.""",
"""Красотка” (Pretty Woman, 1990): “Я хочу, чтобы ты была рядом. Просто рядом.”""",
"""“Реальная любовь” (Love Actually, 2003): “Для меня ты идеальна.”""",
""""“Вам письмо” (You’ve Got Mail, 1998): “Мне кажется, что я влюбился в тебя, еще не встретив тебя.”""",
"""“Гордость и предубеждение” (Pride & Prejudice, 2005): “Вы околдовали меня, телом и душой.”""",
""""“Ходячий замок” (Howl’s Moving Castle, 2004): “Я так долго тебя искал.”""",
"""“Титаник” (Titanic, 1997): “Ты прыгаешь, и я прыгаю, помнишь?”""",
"""“Амели” (Le fabuleux destin d’Amélie Poulain, 2001): “Бывают моменты, когда обычная жизнь становится волшебной.”"""
]


class UserData(StatesGroup):
    used_messages = State()
    used_quotes = State()


# Создаем инлайн кнопки
def create_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Милое сообщение", callback_data="get_cute_message")
    builder.button(text="Фраза из фильма", callback_data="get_movie_quote")
    return builder.as_markup()


# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = create_inline_keyboard()
    await message.answer("Привет! Выбери действие:", reply_markup=keyboard)


# Обработчик нажатия на инлайн кнопку для милых сообщений
@dp.callback_query(lambda c: c.data == "get_cute_message")
async def process_callback_get_cute_message(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    used_messages = await state.get_data()
    used_messages = used_messages.get('used_messages', []) if used_messages else []

    available_messages = [msg for msg in cute_messages if msg not in used_messages]

    if not available_messages:
        used_messages.clear()
        available_messages = cute_messages
        await state.update_data(used_messages=[])

    message = random.choice(available_messages)
    used_messages.append(message)
    await state.update_data(used_messages=used_messages)

    await bot.send_message(chat_id=callback_query.message.chat.id, text=message)

# Обработчик нажатия на инлайн кнопку для фраз из фильмов
@dp.callback_query(lambda c: c.data == "get_movie_quote")
async def process_callback_get_movie_quote(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    used_quotes = await state.get_data()
    used_quotes = used_quotes.get('used_quotes', []) if used_quotes else []

    available_quotes = [quote for quote in movie_quotes if quote not in used_quotes]

    if not available_quotes:
        used_quotes.clear()
        available_quotes = movie_quotes
        await state.update_data(used_quotes=[])

    quote = random.choice(available_quotes)
    used_quotes.append(quote)
    await state.update_data(used_quotes=used_quotes)

    await bot.send_message(chat_id=callback_query.message.chat.id, text=quote)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())