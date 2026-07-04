from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Зарегистрироваться", callback_data="start_registration")]])

profile_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="confirm")], 
        [InlineKeyboardButton(text="Начать заново", callback_data="restart")]])