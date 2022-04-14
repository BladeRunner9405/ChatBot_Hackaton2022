import telebot
import pandas as pd
from telebot import types
import time

bot = telebot.TeleBot('1718860822:AAFjIDyfLAkQgEK0s363vZw8XHnu4Npb8HQ');
db = pd.read_csv('telegram_bot_database_test.csv')
res = ""
pos = ""
password = ""
login = ""
message_ids = []
MasterAdmin_id = 498859473
sellers_list = [int(i) for i in db.loc[db['seller'] == 1]['user_id'] if i != 0]
managers_list = [int(i) for i in db.loc[db['manager'] == 1]['user_id'] if i != 0]
admins_list = [int(i) for i in db.loc[db['admin'] == 1]['user_id'] if i != 0]
is_authorized = []
print(sellers_list)
print(managers_list)
print(admins_list)
'''AdminKeyboard = types.ReplyKeyboardMarkup(True)
AdminKeyboard.row('$settings')
AdminKeyboardSettings = types.ReplyKeyboardMarkup(True)
AdminKeyboardSettings.row('DROP DB')'''
def update_db_user_id(login, user_id):
	database = db.to_dict()
	for index, log in database['login'].items():
		if log == login:
			database['user_id'].update({index: user_id})
			break
	pd.DataFrame(database).to_csv('telegram_bot_database_test.csv', index=False)
@bot.message_handler(commands=['start'])
def send_welcome(message):
	if message.from_user.id not in sellers_list and message.from_user.id not in managers_list and message.from_user.id not in admins_list:
		global message_ids
		message_ids.append(message.id)
		markup = types.InlineKeyboardMarkup()
		buttonA = types.InlineKeyboardButton('ВОЙТИ', callback_data='log_in')
		buttonB = types.InlineKeyboardButton('РЕГИСТРАЦИЯ', callback_data='sign_up')
		markup.row(buttonA)
		markup.row(buttonB)
		a = bot.send_message(message.from_user.id, "Здравствуйте. Я тестовый бот общения с разграничением. Пожалуйста, выберите действие из предложенных ниже", reply_markup=markup)
		message_ids.append(a.message_id)
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
	global message_ids
	markupL = types.InlineKeyboardMarkup()
	buttonL1 = types.InlineKeyboardButton('SELLER', callback_data='seller_log_in')
	buttonL2 = types.InlineKeyboardButton('MANAGER', callback_data='manager_log_in')
	buttonL3 = types.InlineKeyboardButton('ADMIN', callback_data='admin_log_in')
	markupL.row(buttonL1)
	markupL.row(buttonL2)
	markupL.row(buttonL3)	
	markupS = types.InlineKeyboardMarkup()
	buttonS1 = types.InlineKeyboardButton('SELLER', callback_data='seller_sign_up')
	buttonS2 = types.InlineKeyboardButton('MANAGER', callback_data='manager_sign_up')
	buttonS3 = types.InlineKeyboardButton('ADMIN', callback_data='admin_sign_up')
	markupS.row(buttonS1)
	markupS.row(buttonS2)
	markupS.row(buttonS3)
	if str(call.data) == "log_in":
		a = bot.send_message(call.message.chat.id, "LOG IN SEQUENCE")
		message_ids.append(a.message_id)
		a = bot.send_message(call.message.chat.id, "What is your position?", reply_markup=markupL)
		message_ids.append(a.message_id)
		#bot.register_next_step_handler(call.message, get_pos)
	if str(call.data) == "sign_up":
		a = bot.send_message(call.message.chat.id, "SIGN UP SEQUENCE")
		message_ids.append(a.message_id)
		a = bot.send_message(call.message.chat.id, "What is your position?", reply_markup=markupS)
		message_ids.append(a.message_id)
		#bot.register_next_step_handler(call.message, get_pos)
	elif str(call.data) == 'seller_log_in':
		a = bot.send_message(call.message.chat.id, "Your position: " + 'SELLER')
		message_ids.append(a.message_id)
		a = bot.send_message(call.message.chat.id, "Type in your login")
		message_ids.append(a.message_id)
		bot.register_next_step_handler(call.message, Llogin)
	elif str(call.data) == 'manager_log_in':
		a = bot.send_message(call.message.chat.id, "Your position: " + 'MANAGER')
		message_ids.append(a.message_id)
		a = bot.send_message(call.message.chat.id, "Type in your login")
		message_ids.append(a.message_id)
		bot.register_next_step_handler(call.message, Llogin)
	elif str(call.data) == 'admin_log_in':
		a = bot.send_message(call.message.chat.id, "Your position: " + 'ADMIN')
		message_ids.append(a.message_id)
		a = bot.send_message(call.message.chat.id, "Type in your login")
		message_ids.append(a.message_id)
		bot.register_next_step_handler(call.message, Llogin)
	bot.answer_callback_query(call.id)
def Llogin(call):
	global message_ids
	print('Llogin')
	global login
	login = call.text
	message_ids.append(call.id)
	a = bot.send_message(call.chat.id, "Type in your password")
	message_ids.append(a.message_id)
	bot.register_next_step_handler(call, Lpassword)
def Lpassword(call):
	global message_ids
	print('Lpassword')
	global password
	password = call.text
	message_ids.append(call.id)
	authorize(call)
def authorize(idd):
	global message_ids
	print('authorize')
	print(idd)
	global sellers_list
	global managers_list
	global admins_list
	print(login)
	print(password)
	row = db.loc[db['login']==login]
	#print(row)
	#print(int(row.index[0]))
	#print(str(row['password'][int(row.index[0])]))
	#print(str(password))
	if not row.empty:
		if str(row['password'][int(row.index[0])]) == str(password):
			print(idd.from_user.id)
			if db.loc[int(row.index[0]), 'user_id'] == 0:
				db.loc[int(row.index[0]), 'user_id'] = idd.from_user.id
				print(db)
				db.to_csv('telegram_bot_database_test.csv', index=False)
				#update_db_user_id(login, idd.from_user.id)
				if int(row['seller'][int(row.index[0])]):
					sellers_list.append(idd.from_user.id)
				if int(row['manager'][int(row.index[0])]):
					managers_list.append(idd.from_user.id)
				if int(row['admin'][int(row.index[0])]):
					admins_list.append(idd.from_user.id)
				a = bot.send_message(idd.from_user.id, "AUTH SUCCESSFUL")
				message_ids.append(a.message_id)
				for i in message_ids[1:]:
					bot.delete_message(idd.chat.id, i)
					message_ids.remove(i)
				bot.register_next_step_handler(idd, get_text_messages)
			elif db.loc[int(row.index[0]), 'user_id'] != idd.from_user.id:
				a = bot.send_message(idd.from_user.id, "This user is already authorized, contact one of administrators")
				message_ids.append(a.message_id)
				if idd.from_user.id in managers_list or idd.from_user.id in sellers_list:
					for i in admins_list[1:]:
						bot.send_message(i, f"SECURITY WARNING! user {idd.from_user.username} tried to login as another user")
		elif str(row['password'][int(row.index[0])]) != str(password):
			a = bot.send_message(idd.from_user.id, "Incorrect password")
			message_ids.append(a.message_id)
	elif row.empty:
		a = bot.send_message(idd.from_user.id, "No such user")
		message_ids.append(a.message_id)
	print(sellers_list)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message_ids:
		bot.delete_message(message.chat.id, message_ids[0])
		message_ids.pop()
	if message.from_user.id in sellers_list:
		if message.text == '$logout':
			sellers_list.remove(message.from_user.id)
			db.loc[db.loc[db['user_id'] == message.from_user.id].index[0], 'user_id'] = 0
			db.to_csv('telegram_bot_database_test.csv', index=False)
		else:
			print(message)
			for i in sellers_list:
				if i != message.from_user.id:
					bot.send_message(i, f"{message.from_user.first_name}[SELLER]:\n{message.text}")
			for n in managers_list:
				if n != message.from_user.id:
					bot.send_message(n, f"{message.from_user.first_name}[SELLER]:\n{message.text}")
			bot.register_next_step_handler(message, get_text_messages)
	elif message.from_user.id in managers_list:
		if message.text == '$logout':
			managers_list.remove(message.from_user.id)
			db.loc[db.loc[db['user_id'] == message.from_user.id].index[0], 'user_id'] = 0
			db.to_csv('telegram_bot_database_test.csv', index=False)
		else:
			print(message)
			for i in managers_list:
				if i != message.from_user.id:
					bot.send_message(i, f"{message.from_user.first_name}:\n{message.text}")
			bot.register_next_step_handler(message, get_text_messages)
	elif message.from_user.id in admins_list:
		pass
	else:
		a = bot.send_message(message.from_user.id, "You're not authorized. Please type /start and choose 'LOG IN' option")
		message_ids.append(a.message_id)
bot.polling(none_stop=True, interval=0)