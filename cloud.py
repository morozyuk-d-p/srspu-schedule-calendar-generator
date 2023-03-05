#!/usr/bin/env python3
import json
from modules.core import create_calendar
from modules.api import get_student_schedule, get_student_finals

def cloudEntry(event, context):
    params = event['queryStringParameters']
    print(params)
    faculty = params['faculty']
    group = params['group']
    year = int(params['year'])
    if (params['mode'] == 'classes'):
        try:
            schedule = get_student_schedule(
                faculty_id=faculty, year=year, group_id=group)
            calendar = create_calendar(schedule, 'classes')
            return {
                'statusCode': 200,
                'body': calendar.to_ical().decode()
            }
        except KeyError or ValueError:
            return {
                'statusCode': 404
            }
        except:
            return {
                'statusCode': 500
            }

    if (params['mode'] == 'finals'):
        try:
            schedule = get_student_finals(
                faculty_id=faculty, year=year, group_id=group)
            calendar = create_calendar(schedule, 'finals')
            return {
                'statusCode': 200,
                'body': calendar.to_ical().decode()
            }
        except KeyError or ValueError:
            return {
                'statusCode': 404
            }
        except:
            return {
                'statusCode': 500
            }
