from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import as_section, as_key_value, as_marked_list

from tgbot.keyboards.inline import simple_menu_keyboard, my_orders_keyboard, \
    OrderCallbackData
from tgbot.keyboards.reply import keyboard_mainMenu, keyboard_rozdily

menu_router = Router()


@menu_router.message(Command("start"))
async def start_handler(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Привіт, {0.first_name}".format(message.from_user),
                           reply_markup=keyboard_mainMenu)


@menu_router.message(F.text =="➡ Обрати розділ")
async def choose_theme_handler(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Обери розділ", reply_markup=keyboard_rozdily)


@menu_router.message(F.text == "📕 Статистика")
async def stat_handler(message: Message, bot: Bot):
    pass


@menu_router.message(F.text == "🔀 Випадкове питання")
async def random_handler(message: Message, bot: Bot):
    pass
