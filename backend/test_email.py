#!/usr/bin/env python
"""
Test email configuration and SMTP connection
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_case_connect.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured

print("📧 Email Configuration Check")
print("=" * 50)

# Check settings
print(f"\n✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"✓ EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"✓ EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"✓ EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"✓ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"✓ EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

print("\n🔄 Testing SMTP Connection...")
print("=" * 50)

try:
    # Test email sending
    result = send_mail(
        subject='Test Email from Cyber Crime Portal',
        message='This is a test email to verify SMTP configuration is working.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['test@example.com'],
        fail_silently=False,
    )
    print(f"✅ Email send attempt result: {result}")
    print("✅ SMTP Configuration is working correctly!")
    
except Exception as e:
    print(f"❌ SMTP Connection Error: {e}")
    print(f"❌ Error Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
