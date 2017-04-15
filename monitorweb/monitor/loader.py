#!/usr/bin/env python3

"""UniWorXMonitor

loader.py

Author:
    - Changkun Ou <hi@changkun.us>

Lisence: MIT
"""

import json


def load_uniworx_account():
    """Load uniworx account name and passcode

    Returns:
        dict: the account info within a dict
    """
    with open('../data/account.json', encoding='utf-8') as file_obj:
        payload = json.load(file_obj)
    return payload['uniworx']


def load_manager_account():
    """Load uniworx account name and passcode

    Returns:
        dict: the account info within a dict
    """
    with open('../data/account.json', encoding='utf-8') as file_obj:
        payload = json.load(file_obj)
    return payload['manager']


def load_courses():
    """Fetch courses from local file

    Return:
        list: all courses with its status from local file
    """
    try:
        file_obj = open('../data/courses.json', encoding='utf-8')
        courses = json.load(file_obj)
        return courses
    except (IOError, ValueError):
        return []


def load_emails():
    """Fetch subscriber from local file

    Return:
        list: all subscriber email
    """
    with open('../data/users.json', encoding='utf-8') as users:
        payload = json.load(users)
    return payload['users']


def store_changes(changes):
    """Write changes
    Write changes into `log.txt`;

    Args:
        changes (list): all change logs (each line as a string) within a list
    """
    # TODO: fix here from txt to json log
    with open('../data/log.txt', 'a', encoding='utf-8') as file_obj:
        file_obj.write('\n'.join(changes))


def store_courses(courses):
    """Write results
    Modify local records of `courses.json`

    Args:
        courses (dict): actually a json object dump to json file
    """
    with open('../data/courses.json', 'w+', encoding='utf-8') as file_obj:
        json.dump(courses, file_obj, indent=2)
