#python.exe C:\Users\Lenovo\Documents\Projekts\Python\BOT\BOTAY_BOT\THE_BEST\DATABASE\sqlighter.py

import sqlite3
import json
import datetime

from Settings import *

#==================================== Генератор токенов ====================================
def TokenGenerator(data):
	token = '{0}:{1}'.format(
		str(datetime.datetime.now()).replace(' ','').replace(':','').replace('-','').replace('.','')
		, data)
	return token

# Генерирует уникальный реферальный код
def refGenerate():
	number = str(datetime.datetime.now()).replace(' ','').replace(':','').replace('-','').replace('.','')
	ReferalCode = ''
	abc = 'abcdefghijklmnopqrstuvwxyz'
	abc += abc.upper()
	
	i = 0
	c = ''
	while i < len(number):
		c += number[i]
		if (i % 2 != 0):
			c = int(c)
			if(c >= (len(abc))):
				c2 = len(abc) - 1
				c -= c2
				ReferalCode += abc[c]
				ReferalCode += abc[c2]
			else:
				ReferalCode += abc[c]
			c = ''

		i += 1
	return ReferalCode
#===========================================================================================

def ensure_connection(func):
	def inner(*args, **kwargs):
		with sqlite3.connect('DATABASE/users_data.sqlite') as conn:
			res = func(*args, conn = conn, **kwargs)
		return res
	return inner






#============================================ Обработка пользователей ============================================

@ensure_connection
def init_db_users(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS users')

	'''
	user_token - токен пользователя

	page - страница
	data - данные страницы

	rights - права (пользователь, админ, супер-админ)
	session - работает ли с пользователем администратор

	ID соц сетей:
	user_id_vk
	user_id_telegram
	'''

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id 					INTEGER PRIMARY KEY,
			user_token 			TEXT NOT NULL,
			user_id_telegram 	INTEGER,
			page 				TEXT NOT NULL,
			data 				TEXT,

			name 				TEXT,
			text_anket 			TEXT,
			language  			TEXT,
			languages_study  	TEXT
		)
	''')

	# Сохранить изменения
	conn.commit()


@ensure_connection
def universal_db_edit(conn, query:str):
	cursor = conn.cursor()
	cursor.execute(query)



# Проверяет, существует ли пользователь
@ensure_connection
def chek_user(conn, app_from: str, user_id: int):
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	cursor.execute('SELECT COUNT(*) FROM users WHERE {0} = ? LIMIT 1'.format(app), (user_id, ))
	(data, ) = cursor.fetchone()
	if(data == 0):
		return False
	else:
		return True

# Создаёт нового пользователя
@ensure_connection
def create_new_user(conn, app_from: str, user_id: int):
	print('Новый пользователь')
	cursor = conn.cursor()
	app = 'user_id_{0}'.format(app_from)
	token = refGenerate()
	cursor.execute('''INSERT INTO users (
			user_token,
			page,
			{0},
			language
			) VALUES (?, ?, ?, ?)'''.format(app)
			,(token, START_PAGE, user_id, START_LANGUAGE))



#=================================================================================================================

#========================================= Список чатов =========================================

@ensure_connection
def init_db_chats(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS chats')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS chats (
			id 					INTEGER PRIMARY KEY,
			from_user_token 	TEXT NOT NULL,
			to_user_token 		TEXT NOT NULL
		)
	''')

	# Сохранить изменения
	conn.commit()

# Создаёт новый чат
@ensure_connection
def create_new_chat(conn, from_user_token: str, to_user_token: str):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO chats (
			from_user_token,
			to_user_token) VALUES (?, ?)'''
			,(from_user_token, to_user_token))

# Список чатов
@ensure_connection
def chat_list(conn, from_user_token: str):
	print(from_user_token)
	cursor = conn.cursor()
	print('--')
	cursor.execute('''SELECT to_user_token FROM chats WHERE from_user_token = ?''', (from_user_token))
	print('---')
	(data, ) = cursor.fetchall()
	return data

#================================================================================================


#========================================= Сообщения =========================================

@ensure_connection
def init_db_messages(conn, force: bool = False):
	cursor = conn.cursor()

	if(force):
		cursor.execute('DROP TABLE IF EXISTS messages')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS messages (
			id 					INTEGER PRIMARY KEY,
			from_user_token 	TEXT NOT NULL,
			to_user_token 		TEXT NOT NULL,
			message 			TEXT NOT NULL
		)
	''')

	# Сохранить изменения
	conn.commit()

# Создаёт сообщение
@ensure_connection
def send_message(conn, from_user_token: str, to_user_token: str, message: str):
	cursor = conn.cursor()
	cursor.execute('''INSERT INTO messages (
			from_user_token,
			to_user_token, message) VALUES (?, ?, ?)'''
			,(from_user_token, to_user_token, message))


# Список сообщений
@ensure_connection
def messages_list(conn, from_user_token: str, to_user_token: str):
	cursor = conn.cursor()
	cursor.execute('''SELECT message FROM messages WHERE (from_user_token = ? and to_user_token = ?)''', (from_user_token, to_user_token))
	data = cursor.fetchall()
	return data

# Список сообщений
@ensure_connection
def delete_messages_list(conn, from_user_token: str, to_user_token: str):
	cursor = conn.cursor()
	cursor.execute('''DELETE FROM messages WHERE (from_user_token = ? and to_user_token = ?)''', (from_user_token, to_user_token))

#================================================================================================



#===================================== FINDE RANDOM PROFILE =====================================
@ensure_connection
def finde_random_profile(conn, languages_list, self_token):
	if (len(languages_list) == 0):
		return None
	# Формирование списка языков для SQL
	languages_list_str = '('
	zapytaya_test = False
	for l in languages_list:
		if (zapytaya_test):
			languages_list_str += ', '
		zapytaya_test = True

		languages_list_str += f'"{l}"'
	languages_list_str += ')'

	# Формирование запроса
	cursor = conn.cursor()

	req = 'FROM users WHERE (language in {} and user_token != "{}") ORDER BY RANDOM() LIMIT 1'.format(languages_list_str, self_token)

	cursor.execute('SELECT COUNT(*) {}'.format(req))
	(data, ) = cursor.fetchall()[0]
	if (data == 0):
		return None

	
	cursor.execute('SELECT user_token {}'.format(req))
	(data, ) = cursor.fetchone()
	return data
#================================================================================================





#======================================= STANDART QUEARY =======================================

'''
			table_name - название таблицы
			line - строка, которую нужно получить (например дату)
			line_selector - строка, по которой будем искать (например id)
			line_selector_value - значение, по которому будем искать
			data - значение, которое нужно вписать
'''

# Получает указанное поле
@ensure_connection
def get_data(conn, table_name: str, line: str, line_selector: str, line_selector_value: str):
	cursor = conn.cursor()
	cursor.execute(F'SELECT {line} FROM {table_name} WHERE {line_selector} = ?', (line_selector_value, ))
	(data, ) = cursor.fetchone()
	return data

# Получает указанную строку
@ensure_connection
def get_all_data(conn, table_name: str, line_selector: str, line_selector_value: str):
	cursor = conn.cursor()
	cursor.execute(F'SELECT * FROM {table_name} WHERE {line_selector} = ?', (line_selector_value, ))
	#(data, ) = cursor.fetchone()
	data = cursor.fetchone()
	return data

# Получает несколько указанных строк
@ensure_connection
def get_all_data_list(conn, table_name: str, line_selector: str, line_selector_value: str):
	cursor = conn.cursor()
	cursor.execute(F'SELECT * FROM {table_name} WHERE {line_selector} = ?', (line_selector_value, ))
	#(data, ) = cursor.fetchone()
	data = cursor.fetchall()
	return data


# Записывает информацию в указанное поле
@ensure_connection
def set_data(conn, table_name: str, line: str, line_selector: str, line_selector_value: str, data: str):
	cursor = conn.cursor()
	cursor.execute(f'UPDATE {table_name} SET {line} = ? WHERE {line_selector} = ?', (data, line_selector_value))
	conn.commit()

# Получает колличество элементов
@ensure_connection
def get_count(conn, table_name: str, line_selector: str, line_selector_value: str):
	cursor = conn.cursor()
	cursor.execute(F'SELECT COUNT(*) FROM {table_name} WHERE {line_selector} = ?', (line_selector_value, ))
	(data, ) = cursor.fetchall()[0]
	return data

# Удаление элемента
@ensure_connection
def delete_item(conn, table_name: str, line_selector: str, line_selector_value: str):
	cursor = conn.cursor()
	cursor.execute(F'DELETE FROM {table_name} WHERE {line_selector} = ?', (line_selector_value, ))
	return 'OK'
#===============================================================================================





@ensure_connection
def init_db(conn, force: bool = False):
	init_db_users(force = force)
	init_db_chats(force = force)
	init_db_messages(force = force)



if __name__ == '__main__':
	print('Соединение с базой')
	init_db_users(force = False)
	init_db_chats(force = False)