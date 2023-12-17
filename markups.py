from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
btnProfile = KeyboardButton("Профиль")
btnStatistics = KeyboardButton("Моя статистика")
btnEditMsg = KeyboardButton("Поменять сообщение для рефералов")
btnMyText = KeyboardButton("Мой текст")
mainMenu.add(btnProfile, btnStatistics, btnEditMsg, btnMyText)

statMenu = ReplyKeyboardMarkup(resize_keyboard=True)
btnMonth = KeyboardButton("Месяц")
btnYear = KeyboardButton("Год")
btnMainMenu = KeyboardButton("Главное меню")
statMenu.add(btnMonth, btnYear, btnMainMenu)