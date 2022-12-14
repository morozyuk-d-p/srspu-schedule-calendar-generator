#!/usr/bin/env python3
import pytz, uuid
from datetime import datetime
from icalendar import Calendar, Event, Timezone, TimezoneStandard
from .api import get_class_intervals, get_class_types, get_student_schedule, get_update_date

def create_lesson_event(last_updated, class_types, class_ints, lesson, day):
    event = Event()
    event.add('uid', uuid.uuid4())
    event.add('dtstamp', pytz.timezone('Europe/Moscow').localize(datetime.strptime(last_updated, '%Y-%m-%d')))
    event.add('summary', f'{class_types[lesson["type"]]["name"] if lesson["type"] != "-" else ""} "{lesson["discipline"]}"')
    event.add('dtstart', pytz.timezone('Europe/Moscow').localize(datetime.strptime(f"{day} {class_ints[str(lesson['class'])]['start']}", '%Y-%m-%d %H:%M')))
    event.add('dtend', pytz.timezone('Europe/Moscow').localize(datetime.strptime(f"{day} {class_ints[str(lesson['class'])]['end']}", '%Y-%m-%d %H:%M')))
    event.add('location', lesson['auditorium'])
    return event

def create_final_event(last_updated, class_types, class_ints, lesson, day):
    event = Event()
    event.add('uid', uuid.uuid4())
    event.add('dtstamp', pytz.timezone('Europe/Moscow').localize(datetime.strptime(last_updated, '%Y-%m-%d')))
    event.add('summary', f'{class_types[lesson["type"]]["name"] if lesson["type"] != "-" else ""} "{lesson["discipline"]}"')
    event.add('dtstart', pytz.timezone('Europe/Moscow').localize(datetime.strptime(f"{day} {lesson['start']}", '%Y-%m-%d %H:%M')))
    event.add('dtend', pytz.timezone('Europe/Moscow').localize(datetime.strptime(f"{day} {lesson['end']}", '%Y-%m-%d %H:%M')))
    event.add('location', lesson['auditorium'])
    return event

def create_calendar(schedule, schedule_type):
    # Get data
    last_updated = get_update_date()
    class_types = get_class_types()
    class_ints = get_class_intervals()

    # Create calendar
    cal = Calendar()
    cal.add('prodid', '-//Morozyuk Daniil//SRSPU NPI Schedule to iCal converter//')
    cal.add('version', '2.0')

    # Create tzinfo section
    tz = Timezone()
    tz.add('tzid', pytz.timezone('Europe/Moscow'))
    tzst = TimezoneStandard()
    tzst.add('dtstart', pytz.timezone('Europe/Moscow').localize(datetime.strptime(last_updated, '%Y-%m-%d')))
    tzst.add('tzoffsetfrom', pytz.timezone('Europe/Moscow').utcoffset(datetime.now()))
    tzst.add('tzoffsetto', pytz.timezone('Europe/Moscow').utcoffset(datetime.now()))
    tz.add_component(tzst)
    cal.add_component(tz)

    if schedule_type == 'classes':
        # Create events in calendar for every lesson
        for lesson in schedule['classes']:
            if lesson['discipline'] == '-':
                pass
            else:
                for day in lesson['dates']:
                    event = create_lesson_event(last_updated, class_types, class_ints, lesson, day)
                    cal.add_component(event)
        return cal
    elif schedule_type == 'finals':
        for lesson in schedule:
            if lesson['discipline'] == '-':
                pass
            else:
                day = lesson['date']
                event = create_final_event(last_updated, class_types, class_ints, lesson, day)
                cal.add_component(event)
        return cal

if __name__ == '__main__':
    faculty = input('Введите код факультета: ')
    year = int(input('Введите курс: '))
    group = input('введите шифр группы: ')
    schedule = get_student_schedule(faculty, year, group)
    cal = create_calendar(schedule)
    print(cal.to_ical().decode().replace('\r\n', '\n').strip())