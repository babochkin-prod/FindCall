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


class Page_settings():
	def __init__(self):
		self.pageName = 'settings'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = []

		keyboard_line = [
				
				# Заполнить заново
				{'text': languages[language]['pages'][self.pageName]['buttons']['fill_in_again'], 'color': 'secondary', 'callback': 'fill_in_again'},
				# Изменить родной язык
				{'text': languages[language]['pages'][self.pageName]['buttons']['native_language'], 'color': 'secondary', 'callback': 'native_language'},
				# Изменить язык поиска
				{'text': languages[language]['pages'][self.pageName]['buttons']['search_language'], 'color': 'secondary', 'callback': 'search_language'},
				# Изменить текст анкеты
				{'text': languages[language]['pages'][self.pageName]['buttons']['change_text'], 'color': 'secondary', 'callback': 'change_text'},
				# Изменить имя
				{'text': languages[language]['pages'][self.pageName]['buttons']['rename'], 'color': 'secondary', 'callback': 'rename'},
			]
		keyboard.append(keyboard_line)
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

		# Заполнить заново
		if (data == 'fill_in_again'):
			return ImportFromStandart(page = 'select_native_language')

		# Изменить родной язык
		if (data == 'native_language'):
			data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
			data_page['data_page'] = {'local_change': True}
			sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
			return ImportFromStandart(page = 'select_native_language')

		# Изменить родной язык
		if (data == 'search_language'):
			data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
			data_page['data_page'] = {'local_change': True}
			sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
			return ImportFromStandart(page = 'search_language')

		# Изменить текст анкеты
		if (data == 'change_text'):
			data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
			data_page['data_page'] = {'local_change': True}
			sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
			return ImportFromStandart(page = 'change_text')

		# Изменить имя
		if (data == 'rename'):
			data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
			data_page['data_page'] = {'local_change': True}
			sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
			return ImportFromStandart(page = 'rename')

		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		answers = languages[language]['pages'][self.pageName]['text']
		return ImportFromStandart(answers = [answers])
#-----------------------------------------------------------------------------------