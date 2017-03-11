# -*- coding: utf-8 -*-
"""UniWorXMonitor

This script gives you a simple tool to monitor the courses changes on LMU
UniWorX.

Example:
    You can just run the following code to create a courses database on
    the script folder:

        $ python main.py  # this create a `courses.json` for you

    Afterwards, everytime you execute this script, you will get the changes
    from the command line and also from the `log.txt` file if you need check
    the history of changes.

Author:
    - Changkun Ou <hi@changkun.us>

Lisence: MIT
"""

import sys
import json
import requests
from bs4 import BeautifulSoup

# basic info
URL = 'https://uniworx.ifi.lmu.de'
# uniworx action
LOGIN_PARAMS = {'action': 'uniworxLoginDo'}
HOMEPAGE_PARAMS = {'action': 'uniworxStudentHome'}
COURSESREGISTER_PARAMS = {'action': 'uniworxCourseRegister'}


def load_info():
    """Load uniworx account name and passcode

    Returns:
        dict: the account info within a dict
    """
    with open('infos.json') as file_obj:
        payload = json.load(file_obj)
    return payload


def login():
    """Simulate login action

    Returns:
        bool: whether the login is success, False if not

    """
    payload = load_info()
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


def fetch_new_courses_status():
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


def fetch_old_courses_status():
    """Fetch courses from local file

    Return:
        list: all courses with its status from local file
    """
    try:
        file_obj = open('courses.json', 'rb')
        courses = json.load(file_obj)
        return courses
    except (IOError, ValueError):
        return []


def monitor():
    """Compare the website results with local results
    1. Output the changes on console;
    2. Write results
    """
    new_courses = fetch_new_courses_status()
    old_courses = fetch_old_courses_status()

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

    import datetime
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
    stores(changes, new_courses)


def stores(changes, new_courses):
    """Write results
    1. Write changes into `log.txt`;
    2. Modify local records of `courses.json`

    Args:
        changes (list): all change logs (each line as a string) within a list
        new_courses (dict): actually a json object dump to json file
    """
    with open('log.txt', 'a') as file_obj:
        if sys.version_info[0] == 3:
            file_obj.write('\n'.join(changes))
        else:
            for change in changes:
                file_obj.write('\n'+change.encode('utf-8'))
    with open('courses.json', 'w+') as file_obj:
        json.dump(new_courses, file_obj, indent=2)
    print('You can also open `log.txt` and check for changes history.')


def main():
    """Main function
    """
    monitor()


if __name__ == '__main__':
    main()
