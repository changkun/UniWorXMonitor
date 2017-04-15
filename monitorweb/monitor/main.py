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
import loader

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


def monitor():
    """Compare the website results with local results
    1. Output the changes on console;
    2. Write results
    """
    # TODO: fix here that passing new courses to call send email
    new_courses = courses_fetcher()
    old_courses = loader.load_courses()

    # Condition cared: status changed (including new course,
    # and old courses status are switched)
    courses_changed = []
    for semester in new_courses:
        for course in semester['courses']:
            for old_semester in old_courses:
                if old_semester['semester'] == semester['semester']:
                    if course not in old_semester['courses']:
                        courses_changed.append(course)
                    else:
                        continue
    changes = ['\n', 'Check Date:'+str(datetime.datetime.now())]
    if courses_changed:
        print('All new courses:')
        print('---------------')
        changes.append('All new courses:')
        for course in courses_changed:
            if sys.version_info[0] == 3:
                status = course[list(course.keys())[0]].center(14) + \
                         ': ' + list(course.keys())[0]
            else:
                status = course[course.keys()[0]].center(14) + \
                         ': ' + course.keys()[0]
            print(status)
            changes.append(status)
        print('---------------')
    else:
        if old_courses:
            print('No further changes.')
            changes.append('No further changes.')
        else:
            print('Local storage created, you might see new courses \
                   after next execution.')
            changes.append('Local storage created, you might see new \
                   courses after next execution.')
    loader.store_changes(changes)
    loader.store_courses(new_courses)
    print('You can also open `log.txt` and check for changes history.')


def main():
    """Main function
    """
    monitor()


if __name__ == '__main__':
    main()
