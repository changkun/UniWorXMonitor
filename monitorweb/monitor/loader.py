#!/usr/bin/env python3

"""UniWorXMonitor

monitorweb/monitor/loader.py

Author:
    - Changkun Ou <hi@changkun.us>

Lisence: MIT
"""

import os
import json

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))


def load_uniworx_account():
    """Load uniworx account name and passcode

    Returns:
        dict: the account info within a dict
    """
    with open(ABSOLUTE_PATH+'/../data/account.json', encoding='utf-8') as file_obj:
        payload = json.load(file_obj)
    return payload['uniworx']


def load_manager_account():
    """Load uniworx account name and passcode

    Returns:
        dict: the account info within a dict
    """
    with open(ABSOLUTE_PATH+'/../data/account.json', encoding='utf-8') as file_obj:
        payload = json.load(file_obj)
    return payload['manager']


def load_courses():
    """Fetch courses from local file

    Return:
        list: all courses with its status from local file
    """
    try:
        file_obj = open(ABSOLUTE_PATH+'/../data/courses.json', encoding='utf-8')
        courses = json.load(file_obj)
        return courses
    except (IOError, ValueError):
        return []


def load_changes():
    """Fetch changes
    """
    with open(ABSOLUTE_PATH+'/../data/log.json', encoding='utf-8') as file_obj:
        return json.load(file_obj)['latest']


def load_emails():
    """Fetch subscriber from local file

    Return:
        list: all subscriber email
    """
    with open(ABSOLUTE_PATH+'/../data/users.json', encoding='utf-8') as users:
        payload = json.load(users)
    return payload['users']


def store_courses(courses):
    """Write results
    Modify local records of `courses.json`

    Args:
        courses (dict): actually a json object dump to json file
    """
    with open(ABSOLUTE_PATH+'/../data/courses.json', 'w+', encoding='utf-8') as file_obj:
        json.dump(courses, file_obj, indent=2)


def store_changes(changes):
    """Write logs
    """
    with open(ABSOLUTE_PATH+'/../data/log.json', 'r', encoding='utf-8') as file_obj:
        history = json.load(file_obj)
    with open(ABSOLUTE_PATH+'/../data/log.json', 'w', encoding='utf-8') as file_obj:
        history['old'].append(history['latest'])
        history['latest'] = changes
        json.dump(history, file_obj, indent=2)
