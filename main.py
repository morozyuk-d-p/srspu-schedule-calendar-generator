#!/usr/bin/env python3
import json, requests, urllib.parse, pytz, uuid
from datetime import datetime
from icalendar import Calendar, Event, Timezone, TimezoneStandard

# Networking
def get_class_intervals():
    uri = 'https://schedule.npi-tu.ru/api/v1/class-intervals'
    request = requests.get(uri)
    result = request.json()
    return result

def get_class_types():
    uri = 'https://schedule.npi-tu.ru/api/v1/class-types'
    request = requests.get(uri)
    result = request.json()
    return result

def get_schedule(faculty_id, year, group_id):
    uri = f'https://schedule.npi-tu.ru/api/v1/faculties/{faculty_id}/years/{year}/groups/{urllib.parse.quote(group_id)}/schedule'
    request = requests.get(uri)
    result = request.json()
    return result

def get_update_date():
    uri = 'https://schedule.npi-tu.ru/api/v1/last-updated'
    request = requests.get(uri)
    result = request.json()
    return result

def create_event(last_updated, lesson, day):
    event = Event()
    event.add('uid', uuid.uuid4())
    event.add('dtstamp', pytz.timezone('Europe/Moscow').localize(datetime.strptime(last_updated, '%Y-%m-%d')))
    event.add('summary', f'{class_types[lesson["type"]]["name"] if lesson["type"] != "-" else ""} "{lesson["discipline"]}"')
    event.add('dtstart', pytz.timezone('Europe/Moscow').localize(datetime.strptime(f"{day} {class_ints[str(lesson['class'])]['start']}", '%Y-%m-%d %H:%M')))
    event.add('dtend', pytz.timezone('Europe/Moscow').localize(datetime.strptime(f"{day} {class_ints[str(lesson['class'])]['end']}", '%Y-%m-%d %H:%M')))
    event.add('location', lesson['auditorium'])
    return event

# Get data
last_updated = get_update_date()
class_types = get_class_types()
class_ints = get_class_intervals()
schedule = get_schedule('2', 3, 'ПИа')

# Create calendar
cal = Calendar()
cal.add('prodid', '-//Morozyuk Daniil//SRSPU NPI Schedule to iCal converter//')
cal.add('version', '2.0')

# Create tzinfo section
tz = Timezone()
tz.add('tzid', pytz.timezone('Europe/Moscow'))
tzst = TimezoneStandard()
tzst.add('dtstart', datetime(2022, 8, 29, 12, 00, 00, tzinfo=pytz.timezone('Europe/Moscow')))
tzst.add('tzoffsetfrom', pytz.timezone('Europe/Moscow').utcoffset(datetime.now()))
tzst.add('tzoffsetto', pytz.timezone('Europe/Moscow').utcoffset(datetime.now()))
tz.add_component(tzst)
cal.add_component(tz)

# Create events in calendar for every lesson
for lesson in schedule['classes']:
    if lesson['discipline'] == '-':
        pass
    else:
        for day in lesson['dates']:
            event = create_event(last_updated, lesson, day)
            cal.add_component(event)
print(cal.to_ical().decode().replace('\r\n', '\n').strip())

with open('calendar.ics', 'w') as file:
    file.write(cal.to_ical().decode())