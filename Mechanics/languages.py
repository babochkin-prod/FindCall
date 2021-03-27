import os

languages = {}

def languages_fide():
	pass


def languages_fide(path, delimiter = '\\'):
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

				languages_fide('{}{}{}'.format(path, delimiter, file_name))

			# Если это файл
			else:
				if(file_name[-3:] == '.py'):
					file_name = file_name[:-3]
					# Импорт скрипта
					com = 'from {} import {}'.format(str_import_from, file_name)
					exec(com)
					# Занесение ссылки на страницу в список страниц
					com = 'languages.update({1} {3}{0}{3}: {0}.language {2})'.format(file_name, '{', '}', "'")
					exec(com)
					

# Автоматическое подключение страниц
delimiter = '\\'
path = 'languages{}'.format(delimiter)
#print('Start loading languages...')
languages_fide(path, delimiter)
#print('Languages loaded.')


#print(languages)