					

	########################################################################################
	##                                                                                    ##
	##                                                                                    ##
	##                       ██████████████████████████████████████                       ##
    ##                       █████████────█────█────██────█████████                       ##
    ##                       █████████─██─█─██─█─██──█─██─█████████                       ##
    ##                       █████████─██─█────█─██──█────█████████                       ##
    ##                       █████████─██─█─██─█─██──█─██─█████████                       ##
    ##                       █████████────█─██─█────██─██─█████████                       ##
    ##                       ██████████████████████████████████████                       ##
    ##                                                                                    ##
    ##                              Oleg, Alexey, Daria, Anna                             ##
    ##                                                                                    ##
	########################################################################################





import telebot
from telebot import types
from config import TOKEN_telegram as TOKEN
from DATABASE import sqlighter
from Mechanics.PagesManager import *
from Mechanics.mechanic import *
from Settings import *
import pprint
import asyncio

'''
Отправка сообщений
bot.send_message(message.chat.id, 'Привет!')
message.text - текст пользователя

Клавиатура:
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Привет', 'Пока')
bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

https://t.me/CkooperBot?start=123
'''


'''

{'users': [{'user_token': '', 'page': '', 'page_data': '', 'answers': [{'type': '', 'text': '', 'media': []}]}]}

users - список с ответами и переходом на страницу для нескольких пользователей, зависящих от ответа
user_token - токен польователя, которому хотим отправить ответ ('-' - отправить текущему пользователю)
page - страница, на которую нужно отправить пользователя ('-' - не менять страницу)
page_data - параметры страницы пользователя ('-' - не менять параметры)
answers - список ответов
---------------------------
type - обязательный параметр при аудиосообщениях или каруселях. В остальных случаях можно не использовать (
		text - текстовый ответ (можно оставить пустым)
		carousel - карусель
		audio_msg - для аудиосообщений
		answer - заменить этот ответ на все стандартные ответы страницы (предыдущие ответы остаются, меняется только этот)

		alert - высвечивает уведомление (ДЛЯ ТЕЛЕГРАМА)
text - текст сообщения
media - вложения
'''


app_from = 'telegram'

# Создаёт клавиатуру из списка списков
def Create_Keyboard(buttons):
	#print(buttons)
	keyboard = telebot.types.ReplyKeyboardMarkup(True)
	if (type(buttons) == str and buttons == '-'):
		keyboard.row()
	else:
		for line in buttons['keyboard']:
			command = ''
			for i in range(len(line)):
				if(i > 0):
					command += ", "
				command += '"' + line[i]['text'] + '"'

			command = 'keyboard.row({})'.format(command)
			exec(command)
	return keyboard


# Создаёт клавиатуру из списка списков
def Create_Keyboard_Inline(buttons):
	#print(buttons)
	keyboard = telebot.types.InlineKeyboardMarkup()
	if (type(buttons) == str and buttons == '-'):
		keyboard.row()
	else:
		for line in buttons['keyboard']:
			command = ''
			for i in range(len(line)):
				item = 'item{0} = types.InlineKeyboardButton("{1}", callback_data = "{2}")'.format(i, line[i]['text'], line[i]['callback'])
				exec(item)
				if(i > 0):
					command += ", "
				command += f'item{i}'

			command = 'keyboard.add({})'.format(command)
			exec(command)
	return keyboard



def say_alert(bot, data, call_id = 0):
	if (call_id != 0):
		bot.answer_callback_query(callback_query_id = call_id, show_alert = True, text = data['text'])

# Отправляет 1 сообщение 1 пользователю (Финальная точка отправки сообщений)
def one_message(bot, user_id, data, keyboard, message_id = 0, call_id = 0, type_message = '-', new_message = False, text_messege_bot = ''):
	'''
	# Алёрты
	if (type_message == 'alert'):
		if (call_id != 0):
			bot.answer_callback_query(callback_query_id = call_id, show_alert = True, text = data['text'])
	'''

	# Обычное сообщение
	if ((data['type'] == '') or (data['type'] == 'text') or (data['type'] == '-')):
		# Текст сообщения
		text = data['text']
		# Вложения сообщения
		attachments = []
		for attach in data['media']:
			attachments.append('{}{}'.format(attach['type'], attach['link_vk']))

		# Новое сообщение
		if (message_id == 0 or new_message):
			if(keyboard != '-'):
				bot.send_message(user_id, text, reply_markup=keyboard)
			else:
				bot.send_message(user_id, text, reply_markup = None)

		else:
			if (text_messege_bot != text):
				if(keyboard != '-'):
					bot.edit_message_text(chat_id = user_id, message_id = message_id, text = text, reply_markup=keyboard)
				else:
					bot.edit_message_text(chat_id = user_id, message_id = message_id, text = text, reply_markup = None)
			else:
				pass
			
	




# Отвечает на сообщения, создавая нового пользователя, если необходимо
def message_handler(bot, text = '', user_id = 0, message_id = 0, result = '-', call_id = 0, text_messege_bot = ''):
	#text = message.text
	#user_id = message.chat.id
	
	# Проверка наличия пользователя
	test_new_user = sqlighter.chek_user(app_from = app_from, user_id = user_id)
	new_user_text = ''
	# Если новый пользователь
	if not(test_new_user):
		new_user_text = New_User(app_from, user_id)
	
	# Страница, на которой находится пользователь
	page = sqlighter.get_data(table_name = 'users', line = 'page', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)

	
	# Для медиавложений (пока не трогать)
	if((type(result) == str) and (result == '-')):
		if not(test_new_user):
			result = Keyboard_Ansver(page, app_from, user_id)
		else:
			result = Keyboard_Events(app_from, page, user_id, text)



	# Перебор всех пользователей
	for user in result['users']:

		#user_id = message.chat.id
		# Меняем id пользователя, если указан конкретный токен
		if(('user_token' in user) and (user['user_token'] != '-')):
			user_id = sqlighter.get_data(table_name = 'users', line = 'user_id_{}'.format(app_from), line_selector = 'user_token', line_selector_value = user['user_token'])
			# Получает из базы страницу, на которой сейчас находится пользователь
			page = sqlighter.get_data(table_name = 'users', line = 'page', line_selector = 'user_token', line_selector_value = user['user_token'])
		else:
			#user['user_token'] = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)
			pass
		
		# Меняем страницу, если она указана, иначе остаёмся на этой же
		if(('page' in user) and (user['page'] != '-')):
			page = user['page']

			# Перезаписывает у пользователя страницу
			sqlighter.set_data(table_name = 'users', line = 'page', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id, data = page)
		else:
			# Получает из базы страницу, на которой сейчас находится пользователь
			page = sqlighter.get_data(table_name = 'users', line = 'page', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id)

		# Замена данных страницы
		# data_page
		if(user['page_data'] != '-'):
			page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id))
			page_data['data_page'] = user['page_data']
			sqlighter.set_data(table_name = 'users', line = 'data', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id, data = json.dumps(page_data))


		
		answers = user['answers']
		# Если новый пользователь, то подставляем ответы старта
		if not(test_new_user):
			answers = start_messages() + answers
			if(new_user_text != ''):
				answers = [{'type': '-', 'text': new_user_text, 'media': []}] + answers

		ans_alert =	[]
		alert_count = 0
		for ans in answers:
			if (ans['type'] == 'alert'):
				alert_count += 1
				ans_alert.append(ans)
		# Если ответов нет, ответить стандартными
		if ((len(answers) - alert_count) == 0):
			answers = Keyboard_Ansver(page, app_from, user_id)['users'][0]['answers']

		ans_standart = []
		for ans in answers:
			if (ans['type'] != 'alert'):
				ans_standart.append(ans)
			else:
				if (alert_count == 0):
					ans_alert.append(ans)

		# Создаёт клавиатуру для страницы
		#keyboard = Create_Keyboard(Keyboard_keyboards(app_from, page, user_id))
		keyboard_standart = Keyboard_keyboards(app_from, page, user_id)
		if (keyboard_standart['type'] == 'inline'):
			keyboard = Create_Keyboard_Inline(keyboard_standart)
		elif (keyboard_standart['type'] == 'keyboard'):
			keyboard = Create_Keyboard(keyboard_standart)
		keyboard_2 = None

		# Перебор ответов для этого пользователя
		for i in range(len(ans_standart)):
			#answer
			new_message = False
			if (user['user_token'] != '-'):
				new_message = True
			if (i == (len(ans_standart) - 1)):
				keyboard_2 = keyboard
			one_message(bot, user_id, ans_standart[i], keyboard_2, message_id = message_id, call_id = call_id, type_message = ans_standart[i]['type'], new_message = new_message, text_messege_bot = text_messege_bot)

		# Перебор алёртов
		for i in range(len(ans_alert)):
			say_alert(bot, ans_alert[i], call_id = call_id)

	#{'users': [{'user_token': '', 'page': '', 'page_data': '', 'answers': [{'type': '', 'text': '', 'media': []}]}]}
	


def start_bot():
	bot = telebot.TeleBot(TOKEN)
	print('start bot')
	#print(telebot.__version__)


	# ПОЛУЧЕНИЕ НОВЫХ СООБЩЕНИЙ
	@bot.message_handler()
	def start_message(message):
		# Обработчик сообщений
		message_handler(bot, text = message.text, user_id = message.chat.id, )


	@bot.callback_query_handler(func = lambda call: True)
	def callback_inline(call):
		message_handler(bot, text = call.data, user_id = call.from_user.id, message_id = call.message.message_id, call_id = call.id, text_messege_bot = call.message.text)
	

	bot.polling(none_stop=True)


# Старт программы
if __name__ == '__main__':
	print('Inicializ DB')
	# Инициализация базы данных
	sqlighter.init_db(force = False)

	# Запуск бота
	start_bot()