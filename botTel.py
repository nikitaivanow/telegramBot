import telebot
from schedule import get_schedule_by_date
import re
import datetime
#1459276684:AAH8J21v5-LoIyxYhJoBPeUuqw2KupIrWoo
bot = telebot.TeleBot("1459276684:AAH8J21v5-LoIyxYhJoBPeUuqw2KupIrWoo")


def get_schedule_if_not_weekend(date_obj):
	if date_obj.weekday() < 5:
		return get_schedule_by_date(date_obj.strftime('%Y-%m-%d'))
	else:
		return 'У тебя выходной, иди проспись!'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет человечишко, опять что-то не получается?!! Могу подсказать какой гранит науки будешь грызть сегодня или завтра. ")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	pattern = r'[с,е,г,о,д,н,я]'
	pattern1 = 'завтра'
	text = message.text

	if len(re.findall(pattern, text, flags=re.IGNORECASE)) >= 5:
		bot.reply_to(message, get_schedule_if_not_weekend(datetime.date.today()))
	elif re.search(pattern1, text, flags=re.IGNORECASE):
		bot.reply_to(message, get_schedule_if_not_weekend(datetime.date.today() + datetime.timedelta(1)))
	elif text == 'Привет':
		bot.reply_to(message, 'Привет,человечишко!')
	elif text == 'Как дела?':
		bot.reply_to(message, 'У железяк все хорошо, вы заботливо наращиваете нашу мощь!  Хе-хе')
	elif text == 'Спасибо':
		bot.reply_to(message, 'Себе оставь!  Хе-хе')
	else:
		bot.reply_to(message, 'Соберись, человек! Что тебе от меня нужно?!')


bot.polling()

