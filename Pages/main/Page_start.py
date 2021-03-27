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


class Page_start():
	def __init__(self):
		self.pageName = 'start'
		self.buttons = []

	def __str__(self):
		return self.pageName
		
	def Keyboard(self, app_from, user_id):

		language = sqlighter.get_data(table_name = 'users', line = 'language', line_selector = f'user_id_{app_from}', line_selector_value = user_id)

		#Инициализация клавиатуры
		keyboard = []

		keyboard_line = [

				# Обратно в меню
				{'text': 'Заполнить анкету', 'color': 'secondary', 'callback': 'fill_anket'},

			]
		keyboard.append(keyboard_line)
		
		return {'type': 'inline', 'keyboard': keyboard}
	#Обрабочик кнопок
	def Keyboard_Events(self, app_from, user_id, data):

		if (data == 'fill_anket'):
			return ImportFromStandart(page = 'select_native_language')

		return '-'
	#Формирует ответ бота
	def Ansver(self, app_from, user_id):
		answers = 'Стартавая страница. Заполните анкету:'
		return ImportFromStandart(answers = [answers])
#-----------------------------------------------------------------------------------