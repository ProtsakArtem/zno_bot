from aiogram import types

#Main menu -------
btn_gotheme = types.KeyboardButton("➡ Обрати розділ")
btn_random = types.KeyboardButton("🔀 Випадкове питання")
btn_lk = types.KeyboardButton("📕 Статистика")

keyboard_mainMenu = types.ReplyKeyboardMarkup([[btn_gotheme],[btn_random],[btn_lk]], resize_keyboard=True)


#Rozdil menu
btn_14_45_year = types.KeyboardButton("1914 - 1945p.")
btn_45_now = types.KeyboardButton("1945 - 2014p.")
btn_do_16_vik = types.KeyboardButton("Найдавніші часи - XVI ст.")
btn_16_18_vik = types.KeyboardButton("XVI - XVIII ст.")
btn_18_19_vik = types.KeyboardButton("XVIII - XIX cт.")
btn_personalies = types.KeyboardButton("Персоналії")
btn_architecture = types.KeyboardButton("Архітектура")
btn_art = types.KeyboardButton("Мистецтво")
btn_back = types.KeyboardButton("🔙 Головне Меню")
keyboard_rozdily = types.ReplyKeyboardMarkup([[btn_14_45_year],[btn_45_now], [btn_do_16_vik], [btn_16_18_vik], [btn_18_19_vik], [btn_personalies], [btn_architecture], [btn_art], [btn_back]], resize_keyboard=True)