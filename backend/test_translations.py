#!/usr/bin/env python
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'secure_case_connect.settings'
django.setup()

from django.utils.translation import activate, gettext, get_language

# Test with Hindi
activate('hi')
print(f'Current language: {get_language()}')

# Test some translations
test_strings = [
    'UPI/Banking Fraud',
    'Job Fraud',
    'Prevention Tips',
    'Dashboard',
    'Ransomware',
    'Sextortion',
]

for s in test_strings:
    translated = gettext(s)
    print(f'{s:30} -> {translated}')
