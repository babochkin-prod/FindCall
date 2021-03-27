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


# Ищет подходящие профили
def profile_find(app_from, user_id):
	self_token = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
	languages_dict = json.loads(sqlighter.get_data(table_name = 'users', line = 'languages_study', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
	profile = sqlighter.finde_random_profile(languages_list = languages_dict, self_token = self_token)


	return profile

def create_answer(app_from, user_id, pageName):
	page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))
	profile = profile_find(app_from, user_id)
	# Язык пользователя
	language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
	if (profile != None):
		page_data['data_page'].update({'profile': profile})
		# Текст профиля
		text_anket = sqlighter.get_data(table_name = 'users', line = 'text_anket', line_selector = 'user_token', line_selector_value = profile)
		# Готовит ответ
		answers = languages[language]['pages'][pageName]['text'].replace('[profile]', text_anket)
	else:
		page_data['data_page'].update({'profile': 'None'})
		answers = languages[language]['pages'][pageName]['text_none']

	sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(page_data))
	return ImportFromStandart(answers = [answers])



#------------------------------------- Главная -------------------------------------


class Page_view_form():
	def __init__(self):
		self.pageName = 'view_form'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = []
		keyboard_line = []

		page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))

		if (page_data['data_page']['profile'] != 'None'):
			keyboard_line = [

					# Нравиться
					{'text': languages[language]['pages'][self.pageName]['buttons']['like'], 'color': 'secondary', 'callback': 'like'},
					# Не нравиться
					{'text': languages[language]['pages'][self.pageName]['buttons']['dislike'], 'color': 'secondary', 'callback': 'dislike'},
			
				]
			keyboard.append(keyboard_line)
		keyboard_line = [

				# Обратно в меню
				{'text': languages[language]['pages'][self.pageName]['buttons']['menu'], 'color': 'secondary', 'callback': 'menu'},

			]
		keyboard.append(keyboard_line)
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))

		if (data == 'menu'):
			page_data['data_page'].pop('profile')
			sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(page_data))
			return ImportFromStandart(page = 'menu')

		# Нравится
		if (data == 'like'):
			answers_ = {'users': [{'user_token': '-', 'page': self.pageName, 'page_data': page_data, 'answers': []}]}
			# Для текущего пользователя
			user_1 = create_answer(app_from, user_id, self.pageName)['users'][0]
			# Для того, кого лайкнули
			user_token = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
			user_2 = {'user_token': page_data['data_page']['profile'], 'page': 'view_form_liked_me', 'page_data': {'profile': user_token}, 'answers': []}
			
			return {'users': [user_1, user_2]}

		# Не нравится
		if (data == 'dislike'):
			return create_answer(app_from, user_id, self.pageName)

		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		return create_answer(app_from, user_id, self.pageName)
#-----------------------------------------------------------------------------------