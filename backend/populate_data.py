#!/usr/bin/env python
"""
Script to populate test data dynamically
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_case_connect.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from complaints.models import Complaint

print("=" * 60)
print("Cyber Crime System - Test Data Population")
print("=" * 60)

# Check if data exists
existing = Complaint.objects.count()
if existing > 0:
    print(f"\n✓ Database already has {existing} complaints")
    print("Skipping creation of sample data...\n")
else:
    print("\n✓ Creating sample data...")
    
    # Get or create officers
    officer1, _ = CustomUser.objects.get_or_create(
        username='officer_smith',
        defaults={
            'email': 'officer.smith@cybercrime.gov',
            'first_name': 'John',
            'last_name': 'Smith',
            'role': 'officer',
            'is_active': True,
        }
    )
    officer1.set_password('password123')
    officer1.save()
    
    officer2, _ = CustomUser.objects.get_or_create(
        username='officer_jones',
        defaults={
            'email': 'officer.jones@cybercrime.gov',
            'first_name': 'Sarah',
            'last_name': 'Jones',
            'role': 'officer',
            'is_active': True,
        }
    )
    officer2.set_password('password123')
    officer2.save()
    
    # Get or create users
    user1, _ = CustomUser.objects.get_or_create(
        username='john_doe',
        defaults={
            'email': 'john.doe@cybercrime.gov.in',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'user',
            'is_active': True,
        }
    )
    user1.set_password('password123')
    user1.save()
    
    user2, _ = CustomUser.objects.get_or_create(
        username='jane_smith',
        defaults={
            'email': 'jane.smith@cybercrime.gov.in',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'user',
            'is_active': True,
        }
    )
    user2.set_password('password123')
    user2.save()
    
    # Create sample complaints
    complaints_data = [
        {'title': 'Email Account Hacked', 'user': user1, 'cat': 'hacking', 'pri': 'critical', 'status': 'in_progress', 'officer': officer1},
        {'title': 'Online Shopping Fraud', 'user': user1, 'cat': 'online_fraud', 'pri': 'high', 'status': 'resolved', 'officer': officer1},
        {'title': 'Phishing Attack', 'user': user2, 'cat': 'phishing', 'pri': 'high', 'status': 'in_progress', 'officer': officer2},
        {'title': 'Identity Theft', 'user': user2, 'cat': 'identity_theft', 'pri': 'critical', 'status': 'in_progress', 'officer': officer1},
        {'title': 'Ransomware Infection', 'user': user1, 'cat': 'ransomware', 'pri': 'critical', 'status': 'in_progress', 'officer': officer2},
        {'title': 'Data Breach Incident', 'user': user2, 'cat': 'data_breach', 'pri': 'high', 'status': 'pending', 'officer': None},
        {'title': 'Cyberbullying Online', 'user': user1, 'cat': 'cyberbullying', 'pri': 'medium', 'status': 'pending', 'officer': None},
        {'title': 'Unauthorized Payments', 'user': user2, 'cat': 'online_fraud', 'pri': 'medium', 'status': 'assigned', 'officer': officer1},
        {'title': 'Malware Detection', 'user': user1, 'cat': 'hacking', 'pri': 'high', 'status': 'assigned', 'officer': officer2},
        {'title': 'Case Closed Successfully', 'user': user2, 'cat': 'phishing', 'pri': 'medium', 'status': 'closed', 'officer': officer1},
    ]
    
    for data in complaints_data:
        Complaint.objects.get_or_create(
            title=data['title'],
            complainant=data['user'],
            defaults={
                'description': f"Detailed description for {data['title']}",
                'category': data['cat'],
                'priority': data['pri'],
                'status': data['status'],
                'assigned_officer': data['officer'],
                'incident_date': timezone.now() - timedelta(days=7),
                'incident_location': 'Online',
                'affected_system': 'Various',
            }
        )

# Print statistics
print("\n" + "=" * 60)
print("CURRENT DATABASE STATISTICS")
print("=" * 60)

total = Complaint.objects.count()
pending = Complaint.objects.filter(status='pending').count()
assigned = Complaint.objects.filter(status='assigned').count()
in_prog = Complaint.objects.filter(status='in_progress').count()
resolved = Complaint.objects.filter(status='resolved').count()
closed = Complaint.objects.filter(status='closed').count()
unassigned = Complaint.objects.filter(assigned_officer__isnull=True).count()
officers = CustomUser.objects.filter(role='officer').count()
users = CustomUser.objects.filter(role='user').count()

print(f"\nComplaints:")
print(f"  Total Complaints: {total}")
print(f"  Pending (unassigned): {pending}")
print(f"  Assigned: {assigned}")
print(f"  In Progress: {in_prog}")
print(f"  Resolved: {resolved}")
print(f"  Closed: {closed}")
print(f"  Unassigned (no officer): {unassigned}")

print(f"\nUsers:")
print(f"  Officers: {officers}")
print(f"  Regular Users: {users}")

print("\n" + "=" * 60)
print("SYSTEM READY")
print("=" * 60)
print("\nAccess the system at: http://127.0.0.1:8000/")
print("\nTest Credentials:")
print("  Admin: admin / admin123")
print("  User: john_doe / password123")
print("  Officer: officer_smith / password123")
print("\n" + "=" * 60)
