import json
import os

from DATABASE import sqlighter

from Settings import *

#Импорт страниц

'''
Разметка клавиатуры
{'inline': [[], []], 'keyboard': [[{'text': 'text', 'color': 'negative'},], []]}
'''

pages = {}

def Pages_Connect(path, delimiter = '\\'):
	for file_name in os.listdir(path):

		str_import_from = path.replace('{}'.format(delimiter), '.').replace('..', '.')
		if(str_import_from[-1] == '.'):
			str_import_from = str_import_from[0: -1]

		if(file_name != '__pycache__') and (file_name != 'STANDART.py'):

			file=os.path.join(path,file_name)


			# Если это папка
			if os.path.isdir(file):
				com = 'from {} import {}'.format(str_import_from, file_name)
				exec(com)

				Pages_Connect('{}{}{}'.format(path, delimiter, file_name))

			# Если это файл
			else:
				if(file_name[-3:] == '.py'):
					file_name = file_name[:-3]
					# Импорт скрипта
					com = 'from {} import {}'.format(str_import_from, file_name)
					exec(com)
					# Занесение ссылки на страницу в список страниц
					com = 'pages.update({1} {0}.{0}().pageName: {0}.{0}() {2})'.format(file_name, '{', '}')
					exec(com)
					

# Автоматическое подключение страниц
delimiter = '\\'
path = 'Pages{}'.format(delimiter)
print('Start loading pages...')
Pages_Connect(path, delimiter)
print('Pages loaded.')


# Сообщения при старте бота
def start_messages():
	answers = []
	page = '-'
	for i in START_MESSAGES:
		answers.append({'type': '-', 'text': i, 'media': []})

	return answers



#------------------------------------- Выборка страницы -------------------------------------
def Keyboard_keyboards(app_from, page, user_id):
	keyboard_request = pages[page].Keyboard(app_from, user_id)
	return keyboard_request
#--------------------------------------------------------------------------------------------

#------------------------------------- Обработчик нажатий -------------------------------------
def Keyboard_Events(app_from, page, user_id, data):
	p_ = [page]

	if(data == 'ПОМОГИ') or (data == '🆘'):
		sqlighter.set_user_data(app_from = app_from, user_id = user_id, line = 'data', data = '')
		return ['main']

	if not(page in pages):
		page = STANDART_PAGE
		sqlighter.set_data(table_name = 'users', line = 'page', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id, data = page)
	p_ = pages[page].Keyboard_Events(app_from, user_id, data)

	if(p_ == '-'):
		p_ = pages[page].Ansver(app_from, user_id)
	return p_
#----------------------------------------------------------------------------------------------

#------------------------------------- Ответ -------------------------------------
def Keyboard_Ansver(page, app_from, user_id):
	return pages[page].Ansver(app_from, user_id)
#---------------------------------------------------------------------------------

#------------------------------------ Медиосообщение ------------------------------------
def Media_Message(app_from, user_id, page, media_data):
	p_ = [page]
	try:
		p_ = pages[page].Media_Message(app_from, user_id, media_data)
	except Exception as e:
		print(e)
	
	if(p_ != '-'):
		return p_
	else:
		return [page]
#----------------------------------------------------------------------------------------


#------------------------------------ Аудиосообщение ------------------------------------
def Audio_Message(app_from, user_id, page, audio_data):
	p_ = [page]
	try:
		p_ = pages[page].Audio_Message(app_from, user_id, audio_data)
	except Exception as e:
		pass
	
	if(p_ != '-'):
		return p_
	else:
		return [page]
#----------------------------------------------------------------------------------------