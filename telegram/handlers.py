from asyncio.events import TimerHandle
from aiogram.types.inline_keyboard import InlineKeyboardButton
from main_bot import bot, dp
from aiogram.dispatcher.filters import Command, state
from aiogram.types import Message
from config import admin_id
from aiogram.types import callback_query
from aiogram import types
from Question import Test
from aiogram.dispatcher import FSMContext

import car_class
import shelve
# ---------------------------------------------------------------------------
async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")

async def send_to_admin_exit(dp):
    await bot.send_message(chat_id=admin_id, text="Что то пошло не так... бот упал.")

# -----------------------------------------------------------------------------

@dp.message_handler(Command("start_parser"), state=None)
async def get_start(message : Message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    city = []
    
    Novosibirsk = InlineKeyboardButton(text="Новосибирск", callback_data='novosibirsk')
    Irkutsk = InlineKeyboardButton(text="Иркутск", callback_data="irkutsk")
    Moscow = InlineKeyboardButton(text="Мосвка", callback_data="moscow")
    Piter = InlineKeyboardButton(text="Санкт-Петербург", callback_data="spb")
    
    city.append(Novosibirsk)
    city.append(Irkutsk)
    city.append(Moscow)
    city.append(Piter)
    
    for iter in city:
        markup_inline.insert(iter)

    await message.answer("Выберите город", reply_markup=markup_inline)
    await Test.Q1.set()
# @dp.callback_query_handler(text="Novosibirsk")
# async def answer_start(call: callback_query):
#     await call.answer(cache_time=60)
#     await call.message.answer("Парсер для города Новосибирск был запущен, ожидайте!")

@dp.callback_query_handler(state=Test.Q1)
async def answer1(call : callback_query, state : FSMContext):
    answer = call.data
    await state.update_data(
        {'city' : answer}
    )
    # await call.message.answer(f'вы нажали {answer}')
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    price = []
    
    category_1 = InlineKeyboardButton(text="0-100к", callback_data='0-100')
    category_2 = InlineKeyboardButton(text="100к-200к", callback_data='100-200')
    category_3 = InlineKeyboardButton(text="200к-500к", callback_data='200-500')
    category_4 = InlineKeyboardButton(text='500к-900к', callback_data='500-900')
    category_5 = InlineKeyboardButton(text='900к-1500к', callback_data='900-1500')
    category_6 = InlineKeyboardButton(text='1500к-2000к', callback_data='1500-2000')
    
    price.append(category_1)
    price.append(category_2)
    price.append(category_3)
    price.append(category_4)
    price.append(category_5)
    price.append(category_6)
    
    for iter in price:
        markup_inline.insert(iter)
    await call.answer(cache_time=60)
    await call.message.answer('Выберите ценовой диапазон',
                              reply_markup=markup_inline)
    await Test.next()
    
@dp.callback_query_handler(state=Test.Q2)
async def answer2(call : callback_query, state: FSMContext):
    answer = call.data
    await state.update_data(
        {'price' : answer}
    )
    
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    time = []
    
    time_1 = InlineKeyboardButton(text='1 неделя', callback_data='one_week')
    time_2 = InlineKeyboardButton(text="2 недели", callback_data='two_week')
    time_3 = InlineKeyboardButton(text='1 Месяц', callback_data='month')
    time.append(time_1)
    time.append(time_2)
    time.append(time_3)
    
    for iter in time:
        markup_inline.insert(iter)
    
    await call.answer(cache_time=60)
    await call.message.answer('Выберите отрезок времени',
                              reply_markup=markup_inline)
    await Test.next()
    
@dp.callback_query_handler(state=Test.Q3)
async def answer3(call : callback_query, state : FSMContext):
    answer3 = call.data
    data = await state.get_data()
    answer1 = data.get('city')
    answer2 = data.get('price')
    await call.answer(cache_time=60)
    # await call.message.answer(f'Вы выбрали:\nГород: {answer1}\nЦеновой диапазон: {answer2}\nОтрезок времени: {answer3}')
    # ------------------------------------------------------------------------------------------------
    # Вывод информации из файла
    if answer3 == 'one_week':
        time = "одна неделя"
    elif answer3 == 'two_week':
        time = 'две недели'
    elif answer3 == 'month':
        time = 'месяц'
    await call.message.answer(f'Город: {answer1}\nОтрезок времени: {time}\nЦеновой диапазон: {answer2}')
    # await call.message.answer('https://s.auto.drom.ru/photo/pdfyQsaMz4R6JceHS-Y5NzTe3xEYzXph18GEpaXhWfjJBOFpN_A3HTxNUESXlx1UtZx2fT1MEh3ZXGNzwMRuPlKiVYw.jpg')
    with shelve.open(f'analisis/{answer1}/{answer2}/analisis.db') as file:
        rating_list = file[answer3]
        out_list = []
        for item in range(10):
            out_list.append(rating_list[item].output_to_telegram(item, answer3))
        
        for iteration in out_list:
            await call.message.answer(iteration)
    #----------------------------------------------------------------------------------------
    await state.finish()
    
    

# -----------------------------------------------------------------------------

@dp.message_handler(Command("start"))
async def get_info(message : Message):
    await message.answer("Привет, чтоб получить анализ drom.ru, введите \n/start_parser, выберите город и подождите!\n\nDevoloper: Sosnin D.N.\nEmail: sosnin_dienis@mail.ru\nGit: Funny-Code-d")



# ----------------------------------------------------------------------------
@dp.message_handler()
async def echo(message: Message):
    text = f"{message.text} - commands not found"
    await message.answer(text)
