# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Utilities for django-inspectional-registration
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import random

from django.utils.encoding import force_text
from django.utils.six.moves import range
from registration.compat import sha1


def get_site(request):
    """get current ``django.contrib.Site`` instance

    return ``django.contrib.RequestSite`` instance when the ``Site`` is
    not installed.

    """
    try:
        from django.contrib.sites.shortcuts import get_current_site
    except ImportError:
        from django.contrib.sites.models import get_current_site
    return get_current_site(request)


def generate_activation_key(username):
    """generate activation key with username

    originally written by ubernostrum in django-registration_

    .. _django-registration: https://bitbucket.org/ubernostrum/django-registration
    """
    username = force_text(username)
    seed = force_text(random.random())
    salt = sha1(seed.encode('utf-8')).hexdigest()[:5]
    activation_key = sha1((salt+username).encode('utf-8')).hexdigest()
    return activation_key


def generate_random_password(length=10):
    """generate random password with passed length"""
    # Without 1, l, O, 0 because those character are hard to tell
    # the difference between in same fonts
    chars = '23456789abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    password = "".join([random.choice(chars) for i in range(length)])
    return password


from django.core.mail import EmailMultiAlternatives
def send_mail(subject, message, html_message, from_email, recipients):
    email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                to=recipients
             )
    email.attach_alternative(html_message, 'text/html')
    return email.send()
