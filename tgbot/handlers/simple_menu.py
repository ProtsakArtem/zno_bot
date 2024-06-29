from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from tgbot.keyboards.reply import keyboard_mainMenu, keyboard_rozdily

menu_router = Router()

@menu_router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Вітаємо! Оберіть розділ:", reply_markup=keyboard_mainMenu)

@menu_router.message(F.text=="➡ Обрати розділ")
async def show_rozdily(message: Message):
    await message.answer("Оберіть розділ:", reply_markup=keyboard_rozdily)

@menu_router.message(F.text=="🔙 Головне Меню")
async def back_to_main_menu(message: Message):
    await message.answer("Головне Меню", reply_markup=keyboard_mainMenu)
