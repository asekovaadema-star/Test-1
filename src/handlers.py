from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

users_data = {}

from src.keyboards import start_keyboard, profile_inline

router = Router()

class Registration(StatesGroup):
    name = State()
    age = State()
    confirm = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer (
        f"Привет {message.from_user.first_name}, я готов к командам ฅ^•ﻌ•^ฅ" , 
        reply_markup=start_keyboard)
    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        "/start - приветствие \n" \
        "/help - список команд " \
        "/profile - ваш профиль"
    )


@router.message(Command("profile")) 
async def cmd_profile(message: Message):
    user_id = message.from_user.id
    if user_id in users_data:
        info = users_data[user_id]
        await message.answer(
            f"Ваш профиль (=`ω´=):\n"
            "Имя: {info['name']}\n"
            "Возраст: {info['age']}"
        )
    else:
        await message.answer(
            "Вы не прошли регистрацию (=ＴェＴ=), нажмите кнопку ниже",
            reply_markup=start_keyboard
        )

@router.callback_query(F.data == 'start_registration')
async def start_registartion(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Начинаем регистрацию")
    await state.set_state(Registration.name)
    await callback.message.answer ("Ваше имя (^･o･^)ﾉ?")

@router.message(Registration.name)
async def handle_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text) 
    await state.set_state(Registration.age)   
    await message.answer("Сколько вам лет (=｀ェ´=)?")


@router.message(Registration.age)
async def handl_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text)) 
        data = await state.get_data() 
        await state.set_state(Registration.confirm) 
        await message.answer(
            f"Ваши данные ~(=^‥^)/ :\n"
            f"Имя - {data['name']}\n"
            f"Возраст - {data['age']}",
            reply_markup=profile_inline
        )
        await message.answer("Не волнуйтесь возраст - это всего лишь цифра ( ˘•灬•˘ )")
    else:
        await message.answer("Введите возраст числами （╬￣皿￣）")


@router.callback_query(Registration.confirm, F.data == "confirm")
async def confirm_registration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users_data[callback.from_user.id] = data 
    await state.clear()
    await callback.answer("Регистрация завершена")
    await callback.message.answer("Вы зарегистрировались d(>_･ )")

@router.callback_query(Registration.confirm, F.data == "restart")
async def restart_registration(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.name) 
    await callback.answer("Повторная регистрация (°ー°〃)")
    await callback.message.answer("Введите ваше имя (ʘ ͜ʖ ʘ)")