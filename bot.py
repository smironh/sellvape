#1.2 Встречайте!

#1.2-1.5 - фикс багов

#1.6 - когда можно будет выкладывать картинки⛔
#1.6 - статус, продаж, куплено, рейтинг продвца и покупателя⛔

#1.7 - Реф система⛔

import telebot
from telebot import types

import sqlite3
import random
import config
import time

#import models
#from models import *

bot = telebot.TeleBot(config.TOKEN)

admin = config.chat_id
ref_link = 'https://telegram.me/{}?start={}'

@bot.message_handler(commands=['start'])
def send_welcome(message):

	user_id = message.chat.id
	splited = message.text.split()
	if not Users.user_exists(user_id):
		Users.create_user(user_id)
		if len(splited) == 2:
			Users.increase_ref_count(splited[1])

	markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)

	btn1 = types.KeyboardButton("⚡ Профиль")
	btn2 = types.KeyboardButton("🤑 Продать")
	btn3 = types.KeyboardButton("💸 Купить")
	btn4 = types.KeyboardButton("❤ Мои продажи")
	btn5 = types.KeyboardButton("⛔ Пожаловаться")

	markup1.add(btn1, btn2, btn3, btn4, btn5)

	with sqlite3.connect('db.db') as db:
		
		cursor = db.cursor()

		cursor.execute("""
			CREATE TABLE IF NOT EXISTS username(
				ID INT,
				name TEXT,
				city TEXT
			)""")
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS vape(
				product TEXT,
				ID INT,
				productID INTEGER PRIMARY KEY,
				seller TEXT
			)
			""")
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS userban(
				ID INT
			)
		""")
		cursor.execute("SELECT * FROM username WHERE ID=?", (message.chat.id, ))
		info = cursor.fetchone()
		print(info)

		if info is None:


			print('yeah')
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			button1 = types.KeyboardButton("Москва")
			button2 = types.KeyboardButton('Пермь')
			button3 = types.KeyboardButton('ЕКБ')
			button4 = types.KeyboardButton('СПБ')

			markup.add(button1, button2, button3, button4)

			
			#####

			msg = bot.reply_to(message, f'Привет {message.chat.username} ты тут я вижу впервые❤\n\nДля начало введите в каком городе вы живете!', reply_markup=markup)
			bot.register_next_step_handler(msg, database)


		else:
			print('none')
			cursor.execute('SELECT * from userban WHERE ID=?', (message.chat.id, ))
			usrban = cursor.fetchone()

			if usrban is None:

				bot.send_message(message.chat.id, f"""
	Привет {message.chat.username}❤

	Рекомендуем не менять имя во время тово как продаете вейп

	NEW 1.2 
				""", reply_markup=markup1)
			else:
				bot.reply_to(message, '''
Опссссс, походу вы решили порекламится в моем боте

Если хочешь еще отхватить пизды то свяжись со мной - @YeahAlin321
''')

@bot.message_handler(commands=['help'])
def help(message):
	if ifnot(message) == True:
		bot.reply_to(message, '''
	/buy - Купить
	/sell - Продать

	/profile - Профиль

	/mysell - В продаже

	Сейчас бот не популярен и на версии 1.0, но если его распростронять то в будет очень много покупателей(следовательно и продавцов)
	''')
	else:
		send_welcome()


@bot.message_handler(commands=['sell', 'buy'])
def sell(message):
	if ifnot(message) == True:
		a = telebot.types.ReplyKeyboardRemove()

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()

			cursor.execute('SELECT * from userban WHERE ID=?', (message.chat.id, ))
			usrban = cursor.fetchone()
			if usrban is None:

				if message.text == '/sell' or message.text == '🤑 Продать':
					if ifnot(message) == True:
						msg = bot.reply_to(message, 'Напишите о товаре(название, цену, состояние и тд)\n/cancellation чтобы отменить', reply_markup=a)
						bot.register_next_step_handler(msg, sel)
					else:
						send_welcome(message)

				if message.text == '/buy' or message.text == '💸 Купить':
					buy(message)
			else:
				bot.reply_to(message, '''
	Опссссс, походу вы решили порекламится в моем боте

	Если хочешь еще отхватить пизды то свяжись со мной - @YeahAlin321
				''')
	else:
		send_welcome(message)

@bot.message_handler(commands=['ref'])
def get_my_ref(message):
    bot_name = bot.get_me().username
    bot.reply_to(message, text=ref_link.format(bot_name, message.chat.id))


@bot.message_handler(commands=['ref_count'])
def get_my_refs(message):
    count = Users.get_ref_count(message.chat.id)
    bot.reply_to(message, text=f'Count: {count}')


@bot.message_handler(commands=['sells'])
def sells(message):
	command = message.text.split(maxsplit=1)[1]
	adm = str(admin)
	chat_id = str(message.chat.id)

	if chat_id != adm:
		bot.reply_to(message, 'Съебался в страхе пока не уебал')
	else:
		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()

			cursor.execute("SELECT * FROM username WHERE ID=?", (message.chat.id, ))
			city = cursor.fetchone()

			for i in cursor.execute("SELECT * FROM vape WHERE ID=?", (command, )).fetchall():
				bot.reply_to(message, f"""
{i[0]}

Город {city[2]}

Написать - {i[3]}

Product Id - {i[2]}""")

@bot.message_handler(commands=['del'])
def delet(message):
	command = message.text.split(maxsplit=1)[1]

	adm = str(admin)
	chat_id = str(message.chat.id)

	if chat_id != adm:
		bot.reply_to(message, 'Съебался в страхе пока не уебал')
	else:
		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()
			cursor.execute('DELETE FROM vape WHERE productID=?', (command, ))

			bot.reply_to(message, 'Успешно удалено')

@bot.message_handler(commands=['send'])
def sendreklam(message):
	adm = str(admin)
	chat_id = str(message.chat.id)

	if chat_id != adm:
		bot.reply_to(message, 'Съебался в страхе пока не уебал')
	else:

		msg = bot.reply_to(message, 'Напишите сообщение которое хотите отправить')
		bot.register_next_step_handler(msg, startsend)


def startsend(message):
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()
		no = 0
		yes = 0 
		for i in cursor.execute("SELECT ID FROM username").fetchall():
			try:
				bot.send_message(i[0], message.text)
				yes += 1
			except:no += 1
		bot.send_message(admin, f'{yes} - Успешно отправилось\n\n{no} - Ошибка')


@bot.message_handler(commands=['mysell'])
def mysell(message):
	if ifnot(message) == True:

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()

			cursor.execute('SELECT * from userban WHERE ID=?', (message.chat.id, ))
			usrban = cursor.fetchone()

			if usrban is None:

				cursor.execute("SELECT * FROM vape WHERE ID=?", (message.chat.id, ))
				info = cursor.fetchone()

				rang = cursor.execute('SELECT COUNT(*) FROM vape WHERE ID=?', (message.chat.id, ))

				cursor.execute("SELECT * FROM username WHERE ID=?", (message.chat.id, ))
				city = cursor.fetchone()

				markup = types.InlineKeyboardMarkup()
				button1 = types.InlineKeyboardButton("Удалить", callback_data='Del')
				markup.add(button1)

				b = 0

				for i in cursor.execute("SELECT * FROM vape WHERE ID=?", (message.chat.id, )).fetchall():
					bot.reply_to(message, f"""
{i[0]}

Город {city[2]}

Написать - @{i[3]}

Product Id - {i[2]}
""")
					
					b+= 1
				if b == 0:
					bot.reply_to(message, 'У вас нет объявлений!')
				else:
					bot.send_message(message.chat.id, 'Хотите удалить объявления?', reply_markup=markup)


			else:
				bot.reply_to(message, '''
Опссссс, походу вы решили порекламится в моем боте

Если хочешь еще отхватить пизды то свяжись со мной - @YeahAlin321
	''')
	else:
		send_welcome(message)			

@bot.message_handler(commands=['ban'])
def ban(message):
	command = message.text.split(maxsplit=1)[1]
	adm = str(admin)
	chat_id = str(message.chat.id) # думаю это связано с силой земли

	if chat_id != adm:
		bot.reply_to(message, 'Съебался в страхе пока не уебал')

	else:

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()

			cursor.execute('INSERT INTO userban(ID)VALUEs(?)', (command, ))
			bot.reply_to(message, f'Вы успешно забанили юзера - {command}')

@bot.message_handler(commands=['unban'])
def unban(message):
	command = message.text.split(maxsplit=1)[1]
	adm = str(admin)
	chat_id = str(message.chat.id) # думаю это связано с силой земли

	if chat_id != adm:
		bot.reply_to(message, 'Съебался в страхе пока не уебал')

	else:

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()

			cursor.execute('DELETE FROM userban WHERE ID=?', (command, ))
			bot.reply_to(message, f'Вы разбанили забанили юзера - {command}')


@bot.message_handler(commands=['1'])
def seckret(message):
	command = message.text.split(maxsplit=1)[1]
	
	adm = str(admin)
	chat_id = str(message.chat.id)

	if chat_id != adm:
		bot.reply_to(message, 'Съебался в страхе пока не уебал')
	else:

		markup = types.InlineKeyboardMarkup()
		button1 = types.InlineKeyboardButton("Посмотреть объявления", callback_data='check')
		button2 = types.InlineKeyboardButton("Забанить", callback_data='ban')
		markup.add(button1, button2)

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()
			if command == 'db' or command is None:
				with open("db.db","rb") as file:
					f=file.read()
				bot.send_document(config.chat_id, f,"db.db")
			if command == 'info':
				cursor.execute('SELECT COUNT(ID) FROM username')
				rang = cursor.fetchone()

				cursor.execute('SELECT COUNT(product) FROM vape')
				vapes = cursor.fetchone()

				cursor.execute('SELECT COUNT(ID) FROM userban')
				bans = cursor.fetchone()

				bot.reply_to(message, f'''
{rang[0]} - Пользователей
{vapes[0]} - Объявлений
{bans[0]} - Пользователей в бане
''')
			else:
				cursor.execute('SELECT * FROM username WHERE ID=?', (command, ))
				user=  cursor.fetchone()
				bot.reply_to(message, f'''
Чел - @{user[1]}

Посмотреть продажи - /sells {command}
Забанить - /ban {command}
			''', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def location (message):
	if message.location is not None:
		print(message.location)
		print(message)
	else:
		print(message)
		print(message.location)

@bot.message_handler(commands=['profile'])
def profile(message):
	if ifnot(message) == True:

		#bot_name = bot.get_me().username
		#count = Users.get_ref_count(message.chat.id)

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()

			cursor.execute('SELECT * from userban WHERE ID=?', (message.chat.id, ))
			usrban = cursor.fetchone()

			if usrban is None:
				cursor = db.cursor()

				markup = types.InlineKeyboardMarkup()
				button1 = types.InlineKeyboardButton("Изменить данные", callback_data='changecity')
				markup.add(button1)

				cursor.execute("SELECT city FROM username WHERE ID=?", (message.chat.id, ))
				result = cursor.fetchone()
				
				cursor.execute('SELECT COUNT(product) FROM vape WHERE ID=?', (message.chat.id, ))
				rang = cursor.fetchone()

				#count = Users.get_ref_count(message.chat.id)
				#bot_name = bot.get_me().username

				bot.reply_to(message , f"""
Ваш ник - {message.chat.username}
Ваш ID - {message.chat.id}
Город - {result[0]}

Сейчас в продаже - {rang[0]}

""", reply_markup=markup)

			else:
				bot.reply_to(message, '''
Опссссс, походу вы решили порекламится в моем боте

Если хочешь еще отхватить пизды то свяжись со мной - @YeahAlin321
	''')
	else:
		send_welcome(message)

def buy(message):
	if ifnot(message) == True:
		

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()
			
			
			
			cursor.execute('SELECT * from userban WHERE ID=?', (message.chat.id, ))
			usrban = cursor.fetchone()
			if usrban is None:
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

				button1 = types.KeyboardButton("⏩ Далее")
				button2 = types.KeyboardButton('❌ Выйти')
				button3 = types.KeyboardButton("⛔ Пожаловаться")
				
				markup.add(button1, button2, button3)

				with sqlite3.connect('db.db') as db:
					cursor = db.cursor()


					cursor.execute('SELECT * FROM vape ORDER BY RANDOM() LIMIT 1;')
					info = cursor.fetchone()

					cursor.execute('SELECT * FROM username WHERE ID = ?', (info[1],))
					info2 = cursor.fetchone()

					
					try:

						bot.send_message(message.chat.id,  f"""
{info[0]}

В городе {info2[2]}

Написать человеку - @{info[3]}

Product ID - {info[2]}
					""", reply_markup=markup)
					except:
						bot.reply_to(message, f'Произошла ошибка! ProductID - {info[2]} Для жалабы')
			else:
				bot.reply_to(message, '''
Опссссс, походу вы решили порекламится в моем боте

Если хочешь еще отхватить пизды то свяжись со мной - @YeahAlin321
	''')
	else:
		send_welcome(message)


def sel(message):
	markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)

	btn1 = types.KeyboardButton("⚡ Профиль")
	btn2 = types.KeyboardButton("🤑 Продать")
	btn3 = types.KeyboardButton("💸 Купить")
	btn4 = types.KeyboardButton("❤ Мои продажи")
	btn5 = types.KeyboardButton("⛔ Пожаловаться")

	markup1.add(btn1, btn2, btn3, btn4, btn5)
	
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute('SELECT * from userban WHERE ID=?', (message.chat.id, ))
		usrban = cursor.fetchone()
		if usrban is None:

			if message.text == '/cancellation':
				bot.reply_to(message, 'Вы отменили добавление товара', reply_markup=markup1)
			else:
				with sqlite3.connect('db.db') as db:
					cursor = db.cursor()

					data = [
						(message.text, message.chat.id, message.chat.username)
					]

					cursor.executemany('INSERT INTO vape(product, ID, seller)VALUEs(?, ?, ?)', data)
					print(message.content_type)
					if message.content_type == 'photo':
						bot.reply_to(message, 'ВОВОВОВВО Не так быстро! Ты можешь оставить ссылку на картинку!')
					else:

						bot.reply_to(message, 'Вы успешно выложили свой товар! Ждите пока вам напишут', reply_markup=markup1)
		else:
			bot.reply_to(message, '''
Опссссс, походу вы решили порекламится в моем боте

Если хочешь еще отхватить пизды то свяжись со мной - @YeahAlin321
''')


def database(message):
	markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)

	btn1 = types.KeyboardButton("⚡ Профиль")
	btn2 = types.KeyboardButton("🤑 Продать")
	btn3 = types.KeyboardButton("💸 Купить")
	btn4 = types.KeyboardButton("❤ Мои продажи")
	btn5 = types.KeyboardButton("⛔ Пожаловаться")

	markup1.add(btn1, btn2, btn3, btn4, btn5)
	with sqlite3.connect('db.db') as db:
		
		cursor = db.cursor()

		data = [
			(message.chat.id, message.chat.username, message.text, )
		]
		
		cursor.executemany("INSERT INTO username(ID, name, city)VALUEs(?, ?, ?)", data)
		info = cursor.fetchone()


		bot.send_message(admin, f"@{message.from_user.username} Зарегался\n\n{message.from_user.id}")
		bot.reply_to(message, 'Успешно', reply_markup=markup1)


def change(message):

	if message.text == '/cancellation':
		bot.reply_to(message, 'Вы отменили изменение Профиля')
	else:
		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()
			cursor.execute("UPDATE username SET city = ? WHERE id=?", (message.text,message.chat.id,))

			bot.reply_to(message, 'Готово!', reply_markup=markup)
			buy(message)


def exit(message):
	bot.reply_to(message, 'Вы вышли')

	send_welcome(message)
def delete(message):
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()
		cursor.execute("SELECT * from vape WHERE ID= ?", (message.chat.id, ))
		chat_id = (message.chat.id )
		text = (cursor.fetchone()[1])
		print(f'{text}')
		print(chat_id)

		if chat_id == text:
			cursor.execute('DELETE FROM vape WHERE ID=? AND productID=?', (message.chat.id, message.text))

			bot.reply_to(message, f'Вы успешно удалили товар {message.text}')
		if chat_id != text:
			markup = types.InlineKeyboardMarkup()
			button1 = types.InlineKeyboardButton("Указать другой", callback_data='Del')
			markup.add(button1)


			bot.reply_to(message, f'Вы не можете удалить этот товар тк он не ваш!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == "changecity":
			with sqlite3.connect('db.db') as db:
				cursor = db.cursor()

				msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите город')
				print(call.message.chat.id)
				cursor.execute('DELETE FROM username WHERE ID=?', (call.message.chat.id, ))

				bot.register_next_step_handler(msg, database)
		if call.data == 'Del':

			msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Напишите Product Id товара для его удаления')

			bot.register_next_step_handler(msg, delete)
			bot.message_handler(content_types=['text'])
		if call.data == 'complain':
			complain(call.message)

def complain(message):

	if ifnot == True:

		with sqlite3.connect('db.db') as db:
			cursor = db.cursor()

			cursor.execute('SELECT * from userban WHERE ID=?', (message.chat.id, ))
			usrban = cursor.fetchone()

			if usrban is None:
				a = telebot.types.ReplyKeyboardRemove()

				markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)

				btn1 = types.KeyboardButton("⚡ Профиль")
				btn2 = types.KeyboardButton("🤑 Продать")
				btn3 = types.KeyboardButton("💸 Купить")
				btn4 = types.KeyboardButton("❤ Мои продажи")
				btn5 = types.KeyboardButton("⛔ Пожаловаться")

				markup2.add(btn1, btn2, btn3, btn4, btn5)


				msg = bot.reply_to(message, 'Опишите проблему ГЛАВНОЕ НАПИШИТЕ ProductID\n\nЕсли хотите отменить напишите /cancellation', reply_markup=a)

				bot.register_next_step_handler(msg, sendme)

			else:
				bot.reply_to(message, '''
	Опссссс, походу вы решили порекламится в моем боте

	Если хочешь еще отхватить пизды то свяжись со мной - @YeahAlin321
	''')

	else:
		send_welcome()

def sendme(message):
	markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)

	btn1 = types.KeyboardButton("⚡ Профиль")
	btn2 = types.KeyboardButton("🤑 Продать")
	btn3 = types.KeyboardButton("💸 Купить")
	btn4 = types.KeyboardButton("❤ Мои продажи")
	btn5 = types.KeyboardButton("⛔ Пожаловаться")

	markup1.add(btn1, btn2, btn3, btn4, btn5)

	if message.text == '/cancellation':
		bot.reply_to(message, 'Вы отменили жалобу', reply_markup=markup1)
	else:
		bot.send_message(admin, f"{message.text}\n\n")
		bot.reply_to(message, 'Ваша жалоба будет расмотрена', reply_markup=markup1)

def ifnot(message):
	with sqlite3.connect('db.db') as db:
		cursor = db.cursor()

		cursor.execute("SELECT * FROM username WHERE ID=?", (message.chat.id, ))
		info = cursor.fetchone()

		if info is None:
			return False
		else:
			return True

@bot.message_handler()
def allmessage(message):
	if message.text == '❌ Выйти':
		exit(message)
	if message.text == '⏩ Далее':
		buy(message)
	if message.text == '⚡ Профиль':
		profile(message)
	if message.text == '💸 Купить':
		sell(message)
	if message.text == '🤑 Продать':
		sell(message)
	if message.text == '❤ Мои продажи':
		mysell(message)
	if message.text == '⛔ Пожаловаться':
		complain(message)


if __name__ == '__main__':	
	bot.infinity_polling()
	