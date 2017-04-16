#!/usr/bin/env python3

"""UniWorX Monitor

monitorweb/monitor/sendmail.py

Author:
    - Changkun Ou <hi@changkun.us>

Lisence: MIT
"""

import sys
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP
from tqdm import tqdm
from loader import load_emails, load_manager_account, load_changes

HOST = 'mail.changkun.de'
TITLE = {
    'subscribe': 'UniWorX Monitor Subscription Confirmation',
    'unsubscribe': 'UniWorX Monitor Unsubscription Confirmation'
}

CONTENT = {
    'subscribe': """Dear UniWorX Monitor subscriber,

Thanks for your subscribtion, UniWorX Monitor is an open source
project on the GitHub for LMU UniWorX system.

We will send you notification if new UniWorX courses come out.

You can also unsbscribe this service when you don't need it.

If you find any bugs, issue and PR are welcome ;)

---
Best regards,
UniWorX Monitor

website: http://changkun.de/uniworx
github:  https://github.com/changkun/UniWorXMonitor
""",
    'unsubscribe': """Dear UniWorX Monitor subscriber,

You have unsubscribed UniWorX Monitor service, you will no
longer revice our notification anymore.

If you will to subscribe this service again, please visit
our website.

---
Best regards,
UniWorX Monitor

website: http://changkun.de/uniworx
github:  https://github.com/changkun/UniWorXMonitor
"""
}


def dynamic_msg():
    """Construct mail message
    """
    title = 'UniWorX Monitor Notification'
    content = """Dear UniWorX Monitor subscriber,

We notify you that UniWorX launched new courses to apply:
{0}

---
Best regards,
UniWorX Monitor

website: http://changkun.de/uniworx
github:  https://github.com/changkun/UniWorXMonitor
"""
    changes = load_changes()
    courses = """

"""
    for course in changes['apply']:
        print(course)
        courses += course['name'] + '\n'
    return title, content.format(courses)


def send_mail(host, account, passcode, receiver, title, content):
    """Send Email
    """
    # login
    smtp = SMTP(host)
    smtp.ehlo(host)
    smtp.login(account, passcode)
    smtp.set_debuglevel(1)

    # construct message
    email = MIMEText(content, "plain", 'utf-8')
    email["Subject"] = Header(title, 'utf-8')
    email["From"] = account
    email["To"] = receiver
    smtp.sendmail(account, receiver, email.as_string())
    smtp.quit()


def sender(sender_type, email=''):
    """Email sender
    Send email to subscriber.

    Args:
        type (string): three value, all;subscribe;unsubscribe
        email (string): only valid when type is not all
    """
    emails = load_emails()
    account = load_manager_account()['email']
    passcode = load_manager_account()['passcode']

    if sender_type == 'all':
        print('sending...')
        for email in tqdm(emails):
            title, content = dynamic_msg()
            send_mail(HOST, account, passcode, email, title, content)
    else:
        title = TITLE[sender_type]
        content = CONTENT[sender_type]
        send_mail(HOST, account, passcode, email, title, content)
    return 'done'


if __name__ == '__main__':
    print('start sending email...')
    print(sender(sys.argv[1], sys.argv[2]))
    print('emails have been sended')
    sys.stdout.flush()
