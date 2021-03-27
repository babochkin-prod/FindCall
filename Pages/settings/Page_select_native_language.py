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



def languages_list_create():
	languages_list = []
	for l in languages:
		languages_list.append({'language': l, 'language_name': languages[l]['language']})

	return languages_list


#------------------------------------- Главная -------------------------------------


class Page_select_native_language():
	def __init__(self):
		self.pageName = 'select_native_language'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = []
		keyboard_line = []

		languages_list = languages_list_create()

		for l in languages_list:
			keyboard_line.append({'text': l['language_name'], 'color': 'secondary', 'callback': l['language']})
		keyboard.append(keyboard_line)

		'''
		keyboard_line = [
				# Выбор чата
				{'text': languages[language]['pages'][self.pageName]['buttons']['chat_selection'], 'color': 'secondary', 'callback': 'chat_selection'},
				# Смотреть анкеты
				{'text': languages[language]['pages'][self.pageName]['buttons']['view_profiles'], 'color': 'secondary', 'callback': 'view_profiles'},
			]
		keyboard.append(keyboard_line)
		'''

		keyboard_line = [
				# Настройки профиля
				{'text': languages[language]['pages'][self.pageName]['buttons']['apply'], 'color': 'secondary', 'callback': 'apply'},
			]
		keyboard.append(keyboard_line)
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		if (data == 'apply'):
			data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
			if ((data_page['data_page'] != None) and ('local_change' in data_page['data_page'])):
				data_page['data_page'] = {}
				sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
				return ImportFromStandart(page = 'settings')
			else:
				return ImportFromStandart(page = 'rename')

		languages_list = languages_list_create()

		for l in languages_list:
			if (data == l['language']):
				sqlighter.set_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = data)
				return ImportFromStandart()

		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		answers = languages[language]['pages'][self.pageName]['text']
		return ImportFromStandart(answers = [answers])
#-----------------------------------------------------------------------------------