from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_kb():
    kb_list = [
        [KeyboardButton(text="📝 Удалить фон изображения"), KeyboardButton(text="📚 Создать стикерпак")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def second_kb():
    sticker_kb = [
        [KeyboardButton(text="✅ Завершить создание")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=sticker_kb, resize_keyboard=True, one_time_keyboard=True)
    return keyboard