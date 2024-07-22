import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from config import TELEGRAM_TOKEN, CAT_API_TOKEN, NASA_API_TOKEN
import keyboards as kb

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
NASA_API_URL = "https://api.nasa.gov/planetary/apod"

# Функция для получения случайного изображения кота
async def get_cat_image():
    headers = {"x-api-key": CAT_API_TOKEN}
    async with aiohttp.ClientSession() as session:
        async with session.get(CAT_API_URL, headers=headers) as response:
            data = await response.json()
            return data[0]['url']

# Функция для получения информации о картинке дня от NASA
async def get_nasa_apod():
    params = {"api_key": NASA_API_TOKEN}
    async with aiohttp.ClientSession() as session:
        async with session.get(NASA_API_URL, params=params) as response:
            data = await response.json()
            return data['url'], data['title'], data['explanation']

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который может показывать картинки котов и информацию от NASA. Выберите команду ниже:", reply_markup=kb.get_main_menu())

# Обработчик команды /cat
@dp.message(Command('cat'))
async def send_cat_image(message: Message):
    cat_image_url = await get_cat_image()
    await message.answer_photo(cat_image_url, caption="Вот случайный кот!")

# Обработчик команды /nasa
@dp.message(Command('nasa'))
async def send_nasa_apod(message: Message):
    image_url, title, explanation = await get_nasa_apod()
    await message.answer_photo(image_url, caption=f"{title}\n\n{explanation}")

# Обработчик нажатий на инлайн-кнопки
@dp.callback_query(lambda c: c.data in ['cat', 'nasa', 'stop'])
async def process_callback(callback_query: CallbackQuery):
    if callback_query.data == 'cat':
        cat_image_url = await get_cat_image()
        await callback_query.message.answer_photo(cat_image_url, caption="Вот случайный кот!")
    elif callback_query.data == 'nasa':
        image_url, title, explanation = await get_nasa_apod()
        await callback_query.message.answer_photo(image_url, caption=f"{title}\n\n{explanation}")
    elif callback_query.data == 'stop':
        await callback_query.message.answer("Бот остановлен.")
        await bot.close()
        await dp.storage.close()
        await asyncio.sleep(1)  # Добавляем небольшую задержку перед завершением
        loop = asyncio.get_event_loop()
        loop.stop()  # Останавливаем цикл событий
    await callback_query.answer()  # Закрыть всплывающее уведомление

async def main():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Бот остановлен вручную")
    finally:
        # Гарантируем корректное завершение работы бота и хранилища
        await bot.close()
        await dp.storage.close()

if __name__ == '__main__':
    asyncio.run(main())