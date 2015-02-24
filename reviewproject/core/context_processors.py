import os

from reviewproject import settings


def hostname(request):
    return {'hostname': os.getenv('HOSTNAME', None)}


def my_email(request):
    return {'my_email': settings.MY_EMAIL}


def version_number(request):
    return {'version': settings.VERSION}