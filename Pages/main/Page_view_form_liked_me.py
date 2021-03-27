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


def exit(page_data, app_from, user_id, page = 'menu'):
	page_data['data_page'].pop('profile')
	sqlighter.set_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id, data = json.dumps(page_data))
	return ImportFromStandart(page = page)


class Page_view_form_liked_me():
	def __init__(self):
		self.pageName = 'view_form_liked_me'
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
					{'text': '👍', 'color': 'secondary', 'callback': 'like'},
					# Не нравиться
					{'text': '👎', 'color': 'secondary', 'callback': 'dislike'},
			
				]
			keyboard.append(keyboard_line)
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))

		if (data == 'menu'):
			return exit(page_data, app_from, user_id)

		# Нравится
		if (data == 'like'):
			profile = page_data['data_page']['profile']
			user_token = sqlighter.get_data(table_name = 'users', line = 'user_token', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
			sqlighter.create_new_chat(from_user_token = user_token, to_user_token = profile)
			sqlighter.create_new_chat(from_user_token = profile, to_user_token = user_token)
			#return create_answer(app_from, user_id, self.pageName)
			
			return exit(page_data, app_from, user_id, page = 'chats_list')

		# Не нравится
		if (data == 'dislike'):
			return exit(page_data, app_from, user_id)



		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)
		page_data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = f'user_id_{app_from}', line_selector_value = user_id))

		text_form = languages[language]['pages'][self.pageName]['text']
		# Информация профиля
		name_profile = sqlighter.get_data(table_name = 'users', line = 'name', line_selector = 'user_token', line_selector_value = page_data['data_page']['profile'])
		text_anket = sqlighter.get_data(table_name = 'users', line = 'text_anket', line_selector = 'user_token', line_selector_value = page_data['data_page']['profile'])

		answer = f'{text_form}: \n\n{name_profile}:\n {text_anket}'

		return ImportFromStandart(answers = [answer])
#-----------------------------------------------------------------------------------