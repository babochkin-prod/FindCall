
from DATABASE import sqlighter
import datetime


def LOGING_PAY_DATA(TimePay = '', user_token = '', count = 0, type_ = '', type_in = '', pay_outer = '', data = ''):
	if (TimePay == ''):
		TimePay = f'{datetime.datetime.now()}'
	sqlighter.create_payout_log(TimePay = TimePay, user_token = user_token, count = count, type_ = type_, type_in = type_in, pay_outer = pay_outer, data = data)