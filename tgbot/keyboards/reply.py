from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Main menu
btn_gotheme = KeyboardButton(text="➡ Обрати розділ")
btn_random = KeyboardButton(text="🔀 Випадкове питання")
btn_lk = KeyboardButton(text="📕 Статистика")

keyboard_mainMenu = ReplyKeyboardMarkup(
    keyboard=[
        [btn_gotheme],
        [btn_random],
        [btn_lk]
    ],
    resize_keyboard=True
)

# Rozdil menu
btn_14_45_year = KeyboardButton(text="1914 - 1945p.")
btn_45_now = KeyboardButton(text="1945 - 2014p.")
btn_do_16_vik = KeyboardButton(text="Найдавніші часи - XVI ст.")
btn_16_18_vik = KeyboardButton(text="XVI - XVIII ст.")
btn_18_19_vik = KeyboardButton(text="XVIII - XIX cт.")
btn_personalies = KeyboardButton(text="Персоналії")
btn_architecture = KeyboardButton(text="Архітектура")
btn_art = KeyboardButton(text="Мистецтво")
btn_back = KeyboardButton(text="🔙 Головне Меню")

keyboard_rozdily = ReplyKeyboardMarkup(
    keyboard=[
        [btn_14_45_year],
        [btn_45_now],
        [btn_do_16_vik],
        [btn_16_18_vik],
        [btn_18_19_vik],
        [btn_personalies],
        [btn_architecture],
        [btn_art],
        [btn_back]
    ],
    resize_keyboard=True
)
