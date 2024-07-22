# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Случайный кот", callback_data='cat')],
        [InlineKeyboardButton(text="Картинка дня NASA", callback_data='nasa')],
        [InlineKeyboardButton(text="Остановить бота", callback_data='stop')]
    ])
    return keyboard