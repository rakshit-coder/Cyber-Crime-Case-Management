#!/usr/bin/env python
import polib
import os

# Load the .po file
po = polib.pofile('locale/hi/LC_MESSAGES/django.po')

# Create .mo file
po.save_as_mofile('locale/hi/LC_MESSAGES/django.mo')

print(f'Successfully compiled django.po to django.mo')
print(f'Total translations: {len(po)}')
file_size = os.path.getsize('locale/hi/LC_MESSAGES/django.mo')
print(f'File size: {file_size} bytes')
