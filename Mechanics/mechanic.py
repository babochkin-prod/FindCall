import json
from DATABASE import sqlighter
from Settings import *
from Mechanics.Logger import *

import datetime



# Помогает приводить простой список ответов к стандартному виду
def ImportFromStandart(answers = [], page = '-', page_data = '-'):
	answers_ = {'users': [{'user_token': '-', 'page': page, 'page_data': page_data, 'answers': []}]}
	for i in answers:
		answers_['users'][0]['answers'].append({'type': '-', 'text': i, 'media': []})

	return answers_


# Начисление прибыли рефералам (Только в том случае, если пользователь купил аккаунт)
# referal_code - код текущего реферала
# count_in_line - номер в цепочке
def NewUserReferalLink(referal_code, count_in_line = 1):
	if(count_in_line <= len(COEFFICIENTS)):
		COEFFICIENT = COEFFICIENTS[count_in_line - 1]

		# Замена коэффициента на подкрученный
		data = json.loads(sqlighter.get_data(table_name = 'users', line = 'data', line_selector = 'user_token', line_selector_value = referal_code))
		if(('data_weight' in data) and (count_in_line <= len(data['data_weight']))):
			COEFFICIENT = data['data_weight'][count_in_line - 1]

		# Увеличение кол-ва приглашённых людей
		invitations = sqlighter.get_data(table_name = 'users', line = 'invitations', line_selector = 'user_token', line_selector_value = referal_code)
		sqlighter.set_data(table_name = 'users', line = 'invitations', line_selector = 'user_token', line_selector_value = referal_code, data = str(int(invitations) + 1))
		
		# Увеличение прибыли
		earnings = sqlighter.get_data(table_name = 'users', line = 'earnings', line_selector = 'user_token', line_selector_value = referal_code)
		earnings += COEFFICIENT * ACCOUNT_PRICE
		sqlighter.set_data(table_name = 'users', line = 'earnings', line_selector = 'user_token', line_selector_value = referal_code, data = str(earnings))

		# СОХРАНЯЕТ ЛОГ О ТРАНЗАКЦИИ
		LOGING_PAY_DATA(user_token = referal_code, count = COEFFICIENT * ACCOUNT_PRICE, type_ = 'IN', type_in = 'REF', pay_outer = '', data = '')

		# Если есть родительский реферал, вызвать дальше рекурсивно
		referal_code_mather = sqlighter.get_data(table_name = 'users', line = 'referal_mather', line_selector = 'user_token', line_selector_value = referal_code)
		if((referal_code_mather != None) and (referal_code_mather != '')):
			NewUserReferalLink(referal_code_mather, count_in_line = (count_in_line + 1))



# Создаёт нового пользователя. Если перешёл по реф. ссылки, задаёт реферальный код и начисляет прибыль рефералам
def New_User(app_from, user_id, referal_code = '-'):
	sqlighter.create_new_user(app_from = app_from, user_id = user_id)

	data = {'data_page': {}}
	sqlighter.set_data(table_name = 'users', line = 'data', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id, data = json.dumps(data))

	# Если перешёл по реф. ссылки, устанавливает родительского реферала
	'''
	if(referal_code != '-'):
		sqlighter.set_data(table_name = 'users', line = 'referal_mather', line_selector = 'user_id_{}'.format(app_from), line_selector_value = user_id, data = referal_code)
		
		
		# Запускает цепочку рефералов
		#NewUserReferalLink(referal_code)
		
		
		return REFERAL_OK_MES
	'''

	return ''