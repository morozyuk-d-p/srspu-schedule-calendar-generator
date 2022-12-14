#!/usr/bin/env python3
from flask import Flask, render_template, request, abort
from .main import create_calendar
from .api import get_faculties, get_student_schedule, get_student_finals
app = Flask(__name__)

@app.route('/')
def index():
    faculties = get_faculties()
    return render_template('index.html', faculties=faculties)

@app.route('/generate/ics/classes')
def classes_generate():
    faculty, year, group = request.args.get('faculty'), request.args.get('year'), request.args.get('group')
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
    faculty, year, group = request.args.get('faculty'), request.args.get('year'), request.args.get('group')
    try:
        schedule = get_student_finals(faculty_id=faculty, year=year, group_id=group)
        calendar = create_calendar(schedule, 'finals')
        return calendar.to_ical().decode()
    except KeyError or ValueError:
        abort(404)
    except:
        abort(500)