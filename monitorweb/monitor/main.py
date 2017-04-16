#!/usr/bin/env python3

"""UniWorXMonitor

monitorweb/monitor/mail.py

Author:
    - Changkun Ou <hi@changkun.us>

Lisence: MIT
"""

import sys
import datetime
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import loader
import sendmail

# basic info
URL = 'https://uniworx.ifi.lmu.de'
# uniworx action
LOGIN_PARAMS = {'action': 'uniworxLoginDo'}
HOMEPAGE_PARAMS = {'action': 'uniworxStudentHome'}
COURSESREGISTER_PARAMS = {'action': 'uniworxCourseRegister'}


def login():
    """Simulate login action

    Returns:
        bool: whether the login is success, False if not

    """
    payload = loader.load_uniworx_account()
    req = requests.post(URL, params=LOGIN_PARAMS,
                        data=payload, cookies={})
    cookies = {
        'uniworx_session': req.cookies['uniworx_session'],
        'CGISESSID': req.cookies['CGISESSID']
    }
    req = requests.post(URL, params=LOGIN_PARAMS,
                        data=payload, cookies=cookies)
    return True, cookies


def course_register(cookies):
    """Scrach courses register information

    Args:
        cookies (dict): cookies information

    Returns:
        str: html string
    """
    req = requests.post(URL, params=COURSESREGISTER_PARAMS, cookies=cookies)
    return req.text


def courses_fetcher():
    """Fetch courses status from website

    Returns:
        list: All courses with its status from website
    """
    status, cookies = login()
    if status:
        courses_page = course_register(cookies)
        parsed_html = BeautifulSoup(courses_page, 'lxml')

        all_semester_courses = []

        content = parsed_html.find('div', {'id': 'content'})
        children = content.findChildren()

        semester_courses = {
            'semester': None,
            'courses': []
        }
        print('Fetching courses...')
        for child in tqdm(children):
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
                    registerURL = URL + child.select('h4 a')[0]['href']
                    courseURL = None
                    page = requests.post(registerURL).text
                    course_page = BeautifulSoup(page, 'lxml')
                    course_content = course_page.find('div', {'id': 'content'})
                    if len(course_content.select('h1 span a')) is not 0:
                        courseURL = course_content.select('h1 span a')[0]['href']
                    if child.select('.registerBox input'):
                        semester_courses['courses'].append({
                            'name': child.select('h4 a')[0].string,
                            'status': 'Apply',
                            'property': None,
                            'registerURL': registerURL,
                            'courseURL': courseURL
                        })
                    else:
                        semester_courses['courses'].append({
                            'name': child.select('h4 a')[0].string,
                            'status': 'Not Possible',
                            'property': None,
                            'registerURL': registerURL,
                            'courseURL': courseURL
                        })
                elif class_name == 'semester':
                    semester_courses['semester'] = child.string
            except TypeError:
                continue
        print('Done.')
        return all_semester_courses


def monitor(diliver=False):
    """Compare the website results with local results
    1. Output the changes on console;
    2. Write results
    3. send email if diliver is true
    """
    new_courses = courses_fetcher()
    old_courses = loader.load_courses()

    # Condition cared: status changed (including new course,
    # and old courses status are switched)
    courses_changed = {
        'time': str(datetime.datetime.now()),
        'apply': [],
        'not_possible': []
    }
    for semester in new_courses:
        for course in semester['courses']:
            for old_semester in old_courses:
                if old_semester['semester'] == semester['semester']:
                    if course not in old_semester['courses']:
                        if course['status'] == 'Apply':
                            courses_changed['apply'].append(course)
                        else:
                            courses_changed['not_possible'].append(course)
    loader.store_courses(new_courses)
    loader.store_changes(courses_changed)

    if diliver and len(courses_changed['apply']) is not 0:
        sendmail.sender('all')


def main():
    """Main function
    """
    if len(sys.argv) is 2:
        if sys.argv[1] == 'send':
            print('start mail diliver...')
            monitor(diliver=True)
        else:
            print('No new course to diliver...')
            monitor(diliver=False)
    else:
        print("""

        Usage:
        ------
        python3 main.py [send|any_thing_else]

""")


if __name__ == '__main__':
    main()
