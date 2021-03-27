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


def chat_list(user_token):
	buttons = []
	data = sqlighter.get_all_data_list(table_name = 'chats', line_selector = 'from_user_token', line_selector_value = user_token)
	for i in data:
		token_to = i[2]
		name_profile = sqlighter.get_data(table_name = 'users', line = 'name', line_selector = 'user_token', line_selector_value = token_to)
		buttons.append([{'text': name_profile, 'color': 'secondary', 'callback': f'chat_{token_to}'}])

	return buttons



#------------------------------------- Главная -------------------------------------


class Page_chats_list():
	def __init__(self):
		self.pageName = 'chats_list'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		user_token = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = chat_list(user_token)

		keyboard_line = [

				# Меню
				{'text': languages[language]['pages'][self.pageName]['buttons']['menu'], 'color': 'secondary', 'callback': 'menu'},
			]
		keyboard.append(keyboard_line)
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		if (data == 'menu'):
			return ImportFromStandart(page = 'menu')

		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		answers = languages[language]['pages'][self.pageName]['text']
		return ImportFromStandart(answers = [answers])
#-----------------------------------------------------------------------------------