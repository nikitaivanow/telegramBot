import requests
import json
import operator
import datetime
from googletrans import Translator


def create_url(date_string):
    return f'https://tahvel.edu.ee/hois_back/timetableevents/timetableByPerson/\
30P3w1bYb10igyyXeDvh3A?from={date_string}T00:00:00Z&thru={date_string}T00:00:00Z'


def load_schedule_json(url):
    response = requests.get(url)
    return json.loads(response.text)


def try_get_today_schedule(schedule, trans_attempts):
    trans = Translator()
    result_line = ''
    for event in sorted(schedule['timetableEvents'], key=operator.itemgetter('date')):
        base_text = event['nameEn']
        trans_text = base_text
        curr_attempt = 1
        while curr_attempt <= trans_attempts:
            try:
                en_translation = trans.translate(base_text, src='et', dest='ru')
                trans_text = en_translation.text
            except AttributeError:
                curr_attempt += 1
                continue
        result_line += f"{trans_text} - {event['date'][:10]} - {event['timeStart']} - {event['timeEnd']} - Кабинет: {event['rooms'][0]['roomCode']}\n"
    return result_line.rstrip()


def get_schedule_by_date(date_string, trans_attempts: int = 10):
    schedule = load_schedule_json(create_url(date_string))
    return try_get_today_schedule(schedule, trans_attempts)


if __name__ == '__main__':  # Для прямого тестирования модуля schedule.py
    curr_date = datetime.date.today()
    if curr_date.weekday() < 5:  # Если будний день
        print(get_schedule_by_date(curr_date.strftime('%Y-%m-%d')))
    else:  # Если выходной
        print('Ты шо бля?', curr_date.strftime('%Y-%m-%d'))
