'''
-------------- Цветовая палитра кнопок ВК --------------
negative	-	Красный
positive	-	Зелёный
primary		-	Синий
secondary	-	Белый
--------------------------------------------------------

{'type': 'message', 'keyboard': keyboard}
'type' - 'inline' - Клавиатура в сообщении
'type' - 'keyboard'  - Клавиатура снизу
'keyboard' - разметка клавиатуры

'''



from DATABASE import sqlighter
import json
from Settings import *

from Mechanics.languages import *
from Mechanics.mechanic import *



#------------------------------------- Главная -------------------------------------


class Page_chat():
	def __init__(self):
		self.pageName = 'chat'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = []
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
		user_chat_token = page_data['data_page']['profile']
		user_token = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		if (data == '/menu'):
			return ImportFromStandart(page = 'menu')

		# Отправка сообщения
		# Проверка на то, находится ли пользователь в чате, то отправляет ему сообщение
		page = sqlighter.get_data(table_name = 'users', line = 'page', line_selector = 'user_token', line_selector_value = user_chat_token)
		if (page == 'chat'):
			chat_user_chat_token = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = 'user_token', line_selector_value = user_chat_token))['data_page']['profile']
			if (user_token == chat_user_chat_token):
				user = {'user_token': user_chat_token, 'page': '-', 'page_data': '-', 'answers': [{'type': '-', 'text': data, 'media': []}]}
				return {'users': [user]}

		# Иначе сохраняет сообщение в базу
		sqlighter.send_message(from_user_token = user_token, to_user_token = user_chat_token, message = data)
		return {'users': []}

		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
		user_chat_token = page_data['data_page']['profile']
		user_token = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		

		#language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		#answers = languages[language]['pages'][self.pageName]['text']
		answer = 'CHAT\n(For exit to menu send /menu)'

		# Получает список непрочитанных сообщений
		messages = sqlighter.messages_list(from_user_token = user_chat_token, to_user_token = user_token)
		# Удаляет прочитанные сообщения
		sqlighter.delete_messages_list(from_user_token = user_chat_token, to_user_token = user_token)
		# Выводит сообщения
		if (len(messages) > 0):
			answer += '\n\nYour messages:\n\n'
		for message in messages:
			(message_text, ) = message
			answer += '- ' + message_text + '\n'

		return ImportFromStandart(answers = [answer])
#-----------------------------------------------------------------------------------