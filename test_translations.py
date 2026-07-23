#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, 'd:\\secure-case-connect-main\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_case_connect.settings')
django.setup()

from django.utils.translation import get_language, activate
from django.conf import settings
from django.utils.translation import gettext as _

# Test 1: Check available languages
print("✅ Available Languages:")
for code, name in settings.LANGUAGES:
    print(f"  - {code}: {name}")

# Test 2: Check translation files exist
po_file = os.path.join('d:\\secure-case-connect-main\\backend', 'locale/hi/LC_MESSAGES/django.po')
mo_file = os.path.join('d:\\secure-case-connect-main\\backend', 'locale/hi/LC_MESSAGES/django.mo')

print(f"\n✅ Translation Files:")
print(f"  PO file exists: {os.path.exists(po_file)}")
print(f"  MO file exists: {os.path.exists(mo_file)}")
if os.path.exists(mo_file):
    print(f"  MO file size: {os.path.getsize(mo_file)} bytes")

# Test 3: Test actual translation
activate('hi')
print(f"\n✅ Current Language: {get_language()}")

test_strings = [
    "Dashboard",
    "Cyber Awareness Programme",
    "Indian Cyber Crime Laws & Legal Information",
    "Phishing",
    "Types of Cyber Crimes"
]

print(f"\n✅ Test Translations (Hindi):")
for s in test_strings:
    translated = _(s)
    status = "✓" if translated != s else "✗"
    print(f"  {status} '{s}' -> '{translated}'")
