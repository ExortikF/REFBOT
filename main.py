from aiogram import Bot, Dispatcher, executor, types
from config import *
import sqlite3
import markups
from db import Database
from graph_maker import count_date, make_graph_month, make_graph_year
import datetime
from aiogram.types import InputFile
import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('database_ref.db')

#для машины состояний
class Edit_text(StatesGroup):
    waiting_for_text = State()

async def text_start(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Введите текст для своих рефералов:")
    await state.set_state(Edit_text.waiting_for_text.state)

#обработчик fsm
@dp.message_handler(content_types=["text"], state=Edit_text.waiting_for_text)
async def editing_text(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["text"] = message.text

    try:
        f = open(fr"Texts\{message.from_user.id}.txt", "w")
        f.write(f"{message.text}")
        f.close()
        await bot.send_message(message.chat.id, "Вы успешно изменили сообщение на:")
        with open(fr"Texts\{message.from_user.id}.txt") as f:
            text = f.read()
            await bot.send_message(message.chat.id, f"{text}")
    except Exception as er:
        print(er)
        await bot.send_message(message.chat.id, "Возникла какая то ошибка при сохранении текста")
    await message.reply("Вы изменили текст для рефералов!")
    await state.finish()

#обработчик старта
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            date = count_date()
            start_command = message.text
            referrer_id = str(start_command[7:]) #ref id
            if str(referrer_id) != "":
                if str(referrer_id) != str(message.from_user.id):
                    db.add_user(message.from_user.id, date, referrer_id)
                    #Пытаемся открыть текст рефферера
                    try:
                        with open(f"Texts\{referrer_id}".txt) as f:

                            await bot.send_message(message.chat.id, f"{f.read()}")
                    except Exception as er:
                        print(er)
                    try:
                        await bot.send_message(referrer_id, f"По вашей ссылке зарегистрировался новый пользователь!")
                        #тут плюшки для реферрера
                    except:
                        pass
                else:
                    await bot.send_message(message.from_user.id, "Нельзя регистрироваться по собственной ссылке!")
            else:
                db.add_user(message.from_user.id, date)
        await bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=markups.mainMenu)

#обработчик всех текстовых
@dp.message_handler()
async def start_command(message: types.Message):
    if message.chat.type == 'private':
        if message.text == "Профиль" or message.text == "Главное меню":
            await bot.send_message(message.from_user.id, f"ID: {message.from_user.id}\nhttps://t.me/{bot_nickname}?start={message.from_user.id}\nКол-во рефералов: {db.count_referals(message.from_user.id)}", reply_markup=markups.mainMenu)
        if message.text == "Моя статистика":
            await bot.send_message(message.from_user.id, "Выберите, за какой промежуток времени посчитать статистику:", reply_markup=markups.statMenu)
        if message.text == "Месяц":
            if db.count_referals(message.from_user.id) != 0:
                try:
                    make_graph_month(message.from_user.id)
                    photo = InputFile(fr"Temp_graphs\{message.from_user.id}.jpg")
                    await bot.send_message(message.from_user.id, "Ваша статистика за последние 2 месяца:") #Отправляем фото
                    await bot.send_photo(chat_id=message.from_user.id, photo = photo)
                    os.remove(fr"Temp_graphs\{message.from_user.id}.jpg")#удаляем фото
                except Exception as er:
                    await bot.send_message(message.from_user.id, "Ошибка!")
                    print(er)
            else:
                await bot.send_message(message.from_user.id, "У вас нет приглашенных пользователей :(")

        if message.text == "Год":
            if db.count_referals(message.from_user.id) != 0:
                try:
                    make_graph_year(message.from_user.id)
                    photo = InputFile(fr"Temp_graphs\{message.from_user.id}.jpg")
                    await bot.send_message(message.from_user.id, "Ваша статистика за последний год") #Отправляем фото
                    await bot.send_photo(chat_id=message.from_user.id, photo = photo)
                    os.remove(fr"Temp_graphs\{message.from_user.id}.jpg")#удаляем фото
                except Exception as er:
                    await bot.send_message(message.from_user.id, "Ошибка!")
                    print(er)
            else:
                await bot.send_message(message.from_user.id, "У вас нет приглашенных пользователей :(")

        #ИЗМЕНЕНИЕ ТЕКСТА ДЛЯ РЕФЕРАЛА
        if message.text == "Поменять сообщение для рефералов":
            await bot.send_message(message.from_user.id, "Напиши текст, который будет высвечиваться твоим рефералам!")
            await Edit_text.waiting_for_text.set() #состояние ожидания текста

        #Показать свой текст
        if message.text == "Мой текст":
            try:
                with open(f"Texts\{message.from_user.id}.txt") as f:
                    await bot.send_message(message.from_user.id, f"{f.read()}")
            except Exception as er:
                print(er)
                await bot.send_message(message.from_user.id, "Вы ещё не написали свой текст, или бот не может его найти в своей базе данных")






if __name__ == "__main__":
    executor.start_polling(dp)