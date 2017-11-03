import os

from django.utils.text import slugify

from requests import get

from django.conf import settings


def make_slug(department, block, floor, room=""):
    slug = "{} {} {} {}".format(department, block, floor, room)
    return slugify(slug)


def waytosms_credentials():
    file = os.path.join(os.path.dirname(settings.BASE_DIR), 'waytosms.txt')

    with open(file, 'r') as f:
        sender, password = (line.strip() for line in f.readlines())

    return (sender, password)


def send_message(receiver, message):
    frm, password = waytosms_credentials()
    payload = {'Mobile': frm,
               'Password': password,
               'Message': message,
               'To': str(receiver)
               }

    r = get('http://smsapi.engineeringtgr.com/send', params=payload)

    return r.status_code

