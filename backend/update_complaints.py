#!/usr/bin/env python
"""Update complaints with proper status distribution"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_case_connect.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from complaints.models import Complaint
from users.models import CustomUser

# Get officers
officers = list(CustomUser.objects.filter(role='officer'))
if len(officers) < 2:
    print("Error: Need at least 2 officers")
    sys.exit(1)

officer1, officer2 = officers[0], officers[1]

# Get all complaints
complaints = list(Complaint.objects.all())
print(f"\nUpdating {len(complaints)} complaints...\n")

statuses = ['pending', 'assigned', 'in_progress', 'resolved', 'closed']
priorities = ['low', 'medium', 'high', 'critical']

for i, c in enumerate(complaints):
    c.status = statuses[i % len(statuses)]
    c.priority = priorities[i % len(priorities)]
    
    if c.status == 'pending':
        c.assigned_officer = None
    elif i % 2 == 0:
        c.assigned_officer = officer1
    else:
        c.assigned_officer = officer2
    
    c.save()
    print(f"✓ {c.case_number}: {c.status:12} | Priority: {c.priority:8} | Officer: {c.assigned_officer}")

# Print summary
print("\n" + "=" * 70)
print("UPDATED SUMMARY")
print("=" * 70)
print(f"  Pending:      {Complaint.objects.filter(status='pending').count()}")
print(f"  Assigned:     {Complaint.objects.filter(status='assigned').count()}")
print(f"  In Progress:  {Complaint.objects.filter(status='in_progress').count()}")
print(f"  Resolved:     {Complaint.objects.filter(status='resolved').count()}")
print(f"  Closed:       {Complaint.objects.filter(status='closed').count()}")
print(f"  Unassigned:   {Complaint.objects.filter(assigned_officer__isnull=True).count()}")
print("=" * 70)
