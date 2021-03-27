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


class Page_menu():
	def __init__(self):
		self.pageName = 'menu'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = []

		keyboard_line = [
				# Выбор чата
				{'text': languages[language]['pages'][self.pageName]['buttons']['chat_selection'], 'color': 'secondary', 'callback': 'chat_selection'},
				# Смотреть анкеты
				{'text': languages[language]['pages'][self.pageName]['buttons']['view_profiles'], 'color': 'secondary', 'callback': 'view_profiles'},
			]
		keyboard.append(keyboard_line)

		keyboard_line = [
				# Настройки профиля
				{'text': languages[language]['pages'][self.pageName]['buttons']['profile_settings'], 'color': 'secondary', 'callback': 'profile_settings'},
			]
		keyboard.append(keyboard_line)
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		if (data == 'profile_settings'):
			return ImportFromStandart(page = 'settings')

		if (data == 'view_profiles'):
			return ImportFromStandart(page = 'view_form')

		if (data == 'chat_selection'):
			return ImportFromStandart(page = 'chats_list')

		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		answers = languages[language]['pages'][self.pageName]['text']
		return ImportFromStandart(answers = [answers])
#-----------------------------------------------------------------------------------