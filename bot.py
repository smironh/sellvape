#1.1❌
#удаление товара в профиле✔
#удаление товара для меня❌
#бан пользователя❌
#/send❌

#1.0.1✔

import logging
import cfg
import sqlite3
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
    MessageToDeleteNotFound)

logging.basicConfig(level=logging.INFO)

bot = Bot(token = cfg.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
	city = State()
class vape(StatesGroup):
	product = State()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	button1 = KeyboardButton('Пермь')
	button2 = KeyboardButton('Москва')
	button3 = KeyboardButton('Екатеринбург')
	button4 = KeyboardButton('Санкт-Петербург')

	markup= ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(button1, button2, button3, button4)

	btn1 = KeyboardButton('Профиль')
	btn2 = KeyboardButton('Купить')
	btn3 = KeyboardButton('Продать')
	
	markup2= ReplyKeyboardMarkup(resize_keyboard=True)
	markup2.add(btn1, btn2, btn3)



	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute('''
CREATE TABLE IF NOT EXISTS user(
	ID INT,
	forsell INT default(0),
	city TEXT
)
''')
		cursor.execute('''
CREATE TABLE IF NOT EXISTS products(
	ID INT,
	photo TEXT DEFAULT ('NONE'),
	caption TEXT,
	productID INTEGER PRIMARY KEY,
	city TEXT
)
''')
		cursor.execute('SELECT ID FROM user WHERE ID=?', (message.chat.id, ))
		info = cursor.fetchone()

		if info is None:
			await Form.city.set()
			await message.reply("Привет! Я тебя вижу в первые! Напиши или укажи свой Город!", reply_markup=markup)
			
		else:
			await message.answer('Привет! Встречайте 1.0.1!', reply_markup=markup2)

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
	iD = str(message.chat.id)
	myid = str(1020329422)

	if iD == myid:
		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()
			info = cursor.execute('SELECT COUNT(*) FROM user').fetchone()
			await message.reply(f'{info[0]} - Участников')
	else:
		await message.answer('Вам не доступна эта команда')

@dp.message_handler(content_types=['text'])
async def allmessage(message: types.Message):
	if message.text == 'Продать':
		markup = ReplyKeyboardRemove()

		await vape.product.set()
		await message.reply('Можно отправлять только 1 фото!\n\nНапишите о вейпе, можете прикрепить до 1 фото!\n\nДля отмены напишите /close', reply_markup=markup)
	elif message.text == 'Профиль':
		await profile(message)
	elif message.text == 'Купить':
		await buy(message)

@dp.message_handler(state=Form.city)
async def process_name(message: types.Message, state: FSMContext):
	btn1 = KeyboardButton('Профиль')
	btn2 = KeyboardButton('Купить')
	btn3 = KeyboardButton('Продать')
	
	markup2= ReplyKeyboardMarkup(resize_keyboard=True)
	markup2.add(btn1, btn2, btn3)

	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute('INSERT INTO user(ID, city) VALUES(?, ?)', (message.chat.id, message.text, ))

		await message.reply('Вы успешно зарегистрировалиль!', reply_markup=markup2)
		await bot.send_message('1020329422', '+1 пользователь!')
	await state.finish()

@dp.message_handler(state=vape.product, content_types=['photo', 'text'])
async def process_vape(message: types.Message, state=FSMContext):
	btn1 = KeyboardButton('Профиль')
	btn2 = KeyboardButton('Купить')
	btn3 = KeyboardButton('Продать')
	
	markup2= ReplyKeyboardMarkup(resize_keyboard=True)
	markup2.add(btn1, btn2, btn3)
	
	if message.text == '/close':

		await message.reply('Вы успешно отменили добавление товара!', reply_markup=markup2)
	else:
		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()	

			city = cursor.execute('SELECT * FROM user WHERE ID=?', (message.chat.id, )).fetchone()[2]

			if message.content_type == 'photo':
				cursor.execute('INSERT INTO products(photo, caption, city, ID) VALUES(?, ?, ?, ?)', (message.photo[0].file_id, message.caption, city, message.chat.id, ))
				await message.reply('Вы успешно выложили товар, ждите пока вам напишут', reply_markup=markup2)
			if message.content_type == 'text':
				cursor.execute('INSERT INTO products(caption, city, ID) VALUES(?, ?, ?)', (message.text, city, message.chat.id))
				await message.reply('Вы успешно выложили товар, ждите пока вам напишут', reply_markup=markup2)
	await state.finish()

async def profile(message: types.Message):
	inline_btn_1 = InlineKeyboardButton('Мои продажи', callback_data='mysell')
	markup = InlineKeyboardMarkup().add(inline_btn_1)

	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		info = cursor.execute('SELECT * FROM user WHERE ID=?', (message.chat.id, )).fetchone()  

		await message.reply(f'''
{info[0]} - ID
Город - {info[2]}

Реф ссылка - Soon
Рефералов - Soon
''', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'next')
async def next(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await callback_query.message.delete()

	await buy(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'back')
async def back(callback_query: types.CallbackQuery):
	btn1 = KeyboardButton('Профиль')
	btn2 = KeyboardButton('Купить')
	btn3 = KeyboardButton('Продать')
	
	markup2= ReplyKeyboardMarkup(resize_keyboard=True)
	markup2.add(btn1, btn2, btn3)

	await bot.answer_callback_query(callback_query.id)
	await callback_query.message.delete()

	await callback_query.message.answer('Вы успешно вышли!', reply_markup=markup2)
@dp.callback_query_handler(lambda c: c.data == 'not')
async def none(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await callback_query.message.answer('Команда пока не доступна!')

@dp.callback_query_handler(lambda c: c.data == 'mysell')
async def process_callback_del1(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	await callback_query.message.delete()

	btn = InlineKeyboardButton('Удалить', callback_data='delete')
	btn2 = InlineKeyboardButton('Изменить', callback_data='not')
	
	markup = InlineKeyboardMarkup().add(btn, btn2)

	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()


		for vape in cursor.execute('SELECT * FROM products WHERE ID=?', (callback_query.message.chat.id, )).fetchall():
			
			if vape[1] == 'NONE':
				await callback_query.message.answer(f'''
{vape[2]}

{vape[4]}
productId: {vape[3]}
	''', reply_markup=markup)
			else:
				await bot.send_photo(callback_query.message.chat.id, photo = vape[1], caption=f'''
{vape[2]}


{vape[4]}
productId: {vape[3]}
	''', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'delete')
async def delete(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)

	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		try:
			arr = callback_query.message.text.split(': ')
		except:
			arr = callback_query.message.caption.split(': ')
		
		#print(arr[1])

		cursor.execute('DELETE FROM products WHERE productID=?', (arr[1], ))
		await callback_query.message.answer('Вы успешно удалили товар')

		await callback_query.message.delete()
		#await callback_query.message.answer(callback_query.message.text)

async def buy(message: types.Message):
	btn1 = InlineKeyboardButton('Далее', callback_data='next')
	btn2 = InlineKeyboardButton('Выйти', callback_data='back')
	btn3 = InlineKeyboardButton('Пожаловатся', callback_data='not')

	markup = InlineKeyboardMarkup().add(btn1, btn2, btn3)

	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		vape = cursor.execute('SELECT * FROM products ORDER BY RANDOM() LIMIT 1').fetchone()

		if vape[1] == 'NONE':
			await bot.send_message(message.chat.id, f'''
{vape[2]}

{vape[4]}
productId : {vape[3]}
''', reply_markup=markup)
		else:
			await bot.send_photo(message.chat.id, photo = vape[1], caption=f''' 
{vape[2]}

{vape[4]}
ProductId : {vape[3]}
''', reply_markup=markup)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False)