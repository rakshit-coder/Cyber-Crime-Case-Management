#!/usr/bin/env python
"""
Script to check and fix test accounts with example.com emails
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_case_connect.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from users.models import CustomUser

# Check for accounts with example.com emails
test_accounts = CustomUser.objects.filter(email__icontains='example.com')
if test_accounts.exists():
    print(f"Found {test_accounts.count()} accounts with example.com emails:")
    for user in test_accounts:
        print(f"  - {user.username}: {user.email}")
        # Update email to valid test domain
        if user.username == 'john_doe':
            user.email = 'john.doe@cybercrime.gov.in'
            user.save()
            print(f"    ✓ Updated to: {user.email}")
        elif user.username == 'jane_smith':
            user.email = 'jane.smith@cybercrime.gov.in'
            user.save()
            print(f"    ✓ Updated to: {user.email}")
else:
    print("✓ No accounts found with example.com emails")

print("\n✓ Check complete!")
