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


def languages_list_buttons_create(languages_list_db):
	languages_list_buttons = []
	languages_list_buttons_line = []
	for l in languages_list_db:
		languages_list_buttons_line.append({'text': '❌  {}'.format(languages[l]['language']), 'color': 'secondary', 'callback': l})
	languages_list_buttons.append(languages_list_buttons_line)

	return languages_list_buttons


def languages_all_list_buttons():
	languages_list_buttons = []
	languages_list_buttons_line = []

	for l in languages:
		languages_list_buttons_line.append({'text': '{}'.format(languages[l]['language']), 'color': 'secondary', 'callback': l})

	languages_list_buttons.append(languages_list_buttons_line)
	return languages_list_buttons



def keyboard_list_my_languages(app_from, user_id, data_page, page_name):
	language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

	# Инициализация клавиатуры
	keyboard = []
	keyboard_line = []

	keyboard += languages_list_buttons_create(data_page['data_page']['languages_study'])


	keyboard_line = [
				# Добавить язык
				{'text': languages[language]['pages'][page_name]['buttons']['add'], 'color': 'secondary', 'callback': 'add'},
				# Настройки профиля
				{'text': languages[language]['pages'][page_name]['buttons']['apply'], 'color': 'secondary', 'callback': 'apply'},
			]
	#keyboard.append(keyboard_line)

	data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
	if ((data_page['data_page'] != None) and ('local_change' in data_page['data_page'])):

		# Настройки профиля
		keyboard_line.append({'text': languages[language]['pages'][page_name]['buttons']['back'], 'color': 'secondary', 'callback': 'back'},)
		
	keyboard.append(keyboard_line)

	return keyboard


def keyboard_list_languages_select(app_from, user_id, data_page, page_name):
	language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

	# Инициализация клавиатуры
	keyboard = languages_all_list_buttons()
	keyboard_line = []

	keyboard_line = [
				# Настройки профиля
				{'text': languages[language]['pages'][page_name]['buttons']['back'], 'color': 'secondary', 'callback': 'back'},
			]
	keyboard.append(keyboard_line)

	return keyboard

#------------------------------------- Главная -------------------------------------


class Page_search_language():
	def __init__(self):
		self.pageName = 'search_language'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
		#language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		
		if not('language_select' in data_page['data_page']):
			return {'type': 'inline', 'keyboard': keyboard_list_my_languages(app_from, user_id, data_page, page_name = self.pageName)}
		else:
			return {'type': 'inline', 'keyboard': keyboard_list_languages_select(app_from, user_id, data_page, page_name = self.pageName)}

	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))

		if not('language_select' in data_page['data_page']):

			# В меню
			if (data == 'back'):
				if ((data_page['data_page'] != None) and ('local_change' in data_page['data_page'])):
					data_page['data_page'] = {}
					sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
					return ImportFromStandart(page = 'settings')

			data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))

			# Подтвердить
			if (data == 'apply'):
				sqlighter.set_data(table_name = 'users', line = 'languages_study', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page['data_page']['languages_study']))
				if ((data_page['data_page'] != None) and ('local_change' in data_page['data_page'])):
					data_page['data_page'] = {}
					sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
					return ImportFromStandart(page = 'settings')
				else:
					data_page['data_page'] = {}
					sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
					return ImportFromStandart(page = 'menu')

			# Добавить язык
			if (data == 'add'):
				data_page['data_page'].update({'language_select': ''})
				sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
				return ImportFromStandart()

			# Удалить язык
			for l in data_page['data_page']['languages_study']:
				if (data == l):
					data_page['data_page']['languages_study'].pop(l)
					sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
					return ImportFromStandart()

		else:
			if (data == 'back'):
				data_page['data_page'].pop('language_select')
				sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
				return ImportFromStandart()

			for l in languages:
				if (data == l):
					data_page['data_page']['languages_study'].update({l: ''})
					data_page['data_page'].pop('language_select')
					sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
					return ImportFromStandart()



		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		
		data_page = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
		languages_list_db_text = sqlighter.get_data(table_name = 'users', line = 'languages_study', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		if (languages_list_db_text != None and languages_list_db_text != ''):
			languages_list_db = json.loads(languages_list_db_text)
		else:
			languages_list_db = None
		#if ((languages_list_db == None) or (languages_list_db == {})):
		if not('languages_study' in data_page['data_page']):
			data_page['data_page'].update({'languages_study': {}})
			if (languages_list_db != None):
				data_page['data_page']['languages_study'] = languages_list_db
			sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(data_page))
		

		if not('language_select' in data_page['data_page']):
			if ('languages_study' in data_page['data_page']):
				count = len(data_page['data_page']['languages_study'])
			else:
				count = 0
			answers = languages[language]['pages'][self.pageName]['text-1'].replace('[count]', f'{count}')
		else:
			answers = languages[language]['pages'][self.pageName]['text-2']

		return ImportFromStandart(answers = [answers])
#-----------------------------------------------------------------------------------