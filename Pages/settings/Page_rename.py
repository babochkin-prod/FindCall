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


class Page_rename():
	def __init__(self):
		self.pageName = 'rename'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = []
		keyboard_line = []

		data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
		if ((data_page['data_page'] != None) and ('local_change' in data_page['data_page'])):

			keyboard_line = [
					# Настройки профиля
					{'text': languages[language]['pages'][self.pageName]['buttons']['back'], 'color': 'secondary', 'callback': 'back'},
				]
			keyboard.append(keyboard_line)
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))

		if (data == 'back'):
			if ((data_page['data_page'] != None) and ('local_change' in data_page['data_page'])):
				data_page['data_page'] = {}
				sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
				return ImportFromStandart(page = 'settings')

		
		# Сохранение текста в базу данных
		sqlighter.set_data(table_name = 'users', line = 'name', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = data)
		if ((data_page['data_page'] != None) and ('local_change' in data_page['data_page'])):
			return ImportFromStandart(page = 'settings', answers = ['Имя сохранено'])
		else:
			return ImportFromStandart(page = 'change_text')


		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		answers = languages[language]['pages'][self.pageName]['text']
		return ImportFromStandart(answers = [answers])
#-----------------------------------------------------------------------------------