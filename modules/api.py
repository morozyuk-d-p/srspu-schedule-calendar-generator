import requests, urllib.parse

def get_update_date():
    uri = 'https://schedule.npi-tu.ru/api/v1/last-updated'
    request = requests.get(uri)
    result = request.json()
    return result

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

def get_faculties():
    uri = 'https://schedule.npi-tu.ru/api/v1/faculties'
    request = requests.get(uri)
    result = request.json()
    return result

def get_student_schedule(faculty_id, year, group_id):
    uri = f'https://schedule.npi-tu.ru/api/v1/faculties/{faculty_id}/years/{year}/groups/{group_id}/schedule'
    request = requests.get(uri)
    result = request.json()
    return result

def get_student_finals(faculty_id, year, group_id):
    uri = f'https://schedule.npi-tu.ru/api/v1/faculties/{faculty_id}/years/{year}/groups/{group_id}/finals-schedule'
    request = requests.get(uri)
    result = request.json()
    return result