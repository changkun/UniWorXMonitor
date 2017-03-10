# -- coding: utf-8 --
import requests
from bs4 import BeautifulSoup
import json
import csv
import sys

# basic info
url = 'https://uniworx.ifi.lmu.de'
# uniworx action
login_params = {'action':'uniworxLoginDo'}
homepage_params = {'action':'uniworxStudentHome'}
courseRegister_params = {'action':'uniworxCourseRegister'}

def load_info():
  with open('infos.json') as f:
    payload = json.load(f)
  return payload

def login():
  payload = load_info()
  r = requests.post(url, params=login_params, data=payload, cookies={})
  cookies = {
    'uniworx_session':r.cookies['uniworx_session'],
    'CGISESSID': r.cookies['CGISESSID']
  }
  r = requests.post(url, params=login_params, data=payload, cookies=cookies)
  return True, cookies

def course_register(cookies):
  r = requests.post(url, params=courseRegister_params, cookies=cookies)
  return r.text

def fetch_new_courses_status():
  status, cookies = login()
  if status:
    coursesPage = course_register(cookies)
    parsed_html = BeautifulSoup(coursesPage, 'lxml')

    all_semester_courses = []

    content = parsed_html.find('div', {'id':'content'})
    children = content.findChildren()

    semester_courses = {
      'semester': None,
      'courses': []
    }

    for child in children:
      try:
        class_name = child.get('class')[0]
        if class_name == 'spacer':
          all_semester_courses.append(semester_courses)
          semester_courses = semester_courses = {
            'semester': None,
            'courses': []
          }
          continue
        elif class_name == 'indent':
          if child.select('.registerBox input'):
            semester_courses['courses'].append({
              child.select('h4 a')[0].string: 'Apply'
            })
          else:
            semester_courses['courses'].append({
              child.select('h4 a')[0].string: 'Not Possible'
            })
        elif class_name == 'semester':
          semester_courses['semester'] = child.string
        else:
          continue
      except TypeError:
        continue
    return all_semester_courses

def fetch_old_courses_status():
  try:
    f = open('courses.json', 'rb')
    courses = json.load(f)
    return courses 
  except (IOError, ValueError):
    return []

def monitor():
  new_courses = fetch_new_courses_status()
  old_courses = fetch_old_courses_status()

  # Condition cared: status changed (including new course, and old courses status are switched)
  courses_changed = []
  for semester in new_courses:
    for course in semester['courses']:
      for old_semester in old_courses:
        if old_semester['semester'] == semester['semester']:
          if course not in old_semester['courses']:
            courses_changed.append(course)
          else: 
            continue

  import datetime
  changes = ['\n', 'Check Date:'+str(datetime.datetime.now())]
  if courses_changed:
    print('All new courses:')
    print('---------------')
    changes.append('All new courses:')
    for course in courses_changed:
      if sys.version_info[0] == 3:
        status = course[list(course.keys())[0]].center(14) + ': ' + list(course.keys())[0]
      else:
        status = course[course.keys()[0]].center(14) + ': ' + course.keys()[0]
      print(status)
      changes.append(status)
    print('---------------')
  else:
    if old_courses:
      print('No further changes.')
      changes.append('No further changes.')
    else:
      print('Local storage created, you might see new courses after next execution.')
      change.append('Local storage created, you might see new courses after next execution.')

  with open('log.txt', 'a') as f:
    if sys.version_info[0] == 3:
      f.write('\n'.join(changes))
    else:
      for change in changes:
        f.write('\n'+change.encode('utf-8'))
  with open('courses.json', 'w+') as f:
    json.dump(new_courses, f, indent=2) 
  print('You can also open `log.txt` and check for changes history.')


def main():
  monitor()

if __name__ == '__main__':
  main()