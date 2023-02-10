#!/usr/bin/env python3
import base64, urllib.parse
from flask import Flask, render_template, request, abort
from modules.core import create_calendar
from modules.api import get_faculties, get_student_schedule, get_student_finals
app = Flask(__name__)

@app.route('/')
def index():
    faculties = get_faculties()
    return render_template('index.html', faculties=faculties)

@app.route('/generate/ics/classes')
def classes_generate():
    faculty, year, group = request.args.get('faculty'), request.args.get('year'), urllib.parse.quote_from_bytes(base64.decodebytes(request.args.get('group').encode('utf-8')))
    try:
        schedule = get_student_schedule(faculty_id=faculty, year=year, group_id=group)
        calendar = create_calendar(schedule, 'classes')
        return calendar.to_ical().decode()
    except KeyError or ValueError:
        abort(404)
    except:
        abort(500)

@app.route('/generate/ics/finals')
def finals_generate():
    faculty, year, group = request.args.get('faculty'), request.args.get('year'), urllib.parse.quote_from_bytes(base64.decodebytes(request.args.get('group').encode('utf-8')))
    try:
        schedule = get_student_finals(faculty_id=faculty, year=year, group_id=group)
        calendar = create_calendar(schedule, 'finals')
        return calendar.to_ical().decode()
    except KeyError or ValueError:
        abort(404)
    except:
        abort(500)