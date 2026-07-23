"""
Management command to create sample data for testing.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from users.models import CustomUser
from complaints.models import Complaint
from cases.models import CaseWorkflow


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Check if data already exists
        if Complaint.objects.count() > 0:
            self.stdout.write(self.style.WARNING('Data already exists. Skipping creation.'))
            return

        # Get or create officers
        officer1, created = CustomUser.objects.get_or_create(
            username='officer_smith',
            defaults={
                'email': 'officer.smith@cybercrime.gov',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'officer',
                'is_active': True,
            }
        )
        if created:
            officer1.set_password('password123')
            officer1.save()

        officer2, created = CustomUser.objects.get_or_create(
            username='officer_jones',
            defaults={
                'email': 'officer.jones@cybercrime.gov',
                'first_name': 'Sarah',
                'last_name': 'Jones',
                'role': 'officer',
                'is_active': True,
            }
        )
        if created:
            officer2.set_password('password123')
            officer2.save()

        # Get regular users
        try:
            user1 = CustomUser.objects.get(username='john_doe')
        except:
            user1 = CustomUser.objects.create_user(
                username='john_doe',
                email='john.doe@cybercrime.gov.in',
                first_name='John',
                last_name='Doe',
                password='password123',
                role='user'
            )

        try:
            user2 = CustomUser.objects.get(username='jane_smith')
        except:
            user2 = CustomUser.objects.create_user(
                username='jane_smith',
                email='jane.smith@cybercrime.gov.in',
                first_name='Jane',
                last_name='Smith',
                password='password123',
                role='user'
            )

        # Create sample complaints with various statuses
        complaints_data = [
            {
                'complainant': user1,
                'title': 'Email Account Compromised',
                'description': 'My Gmail account was accessed from an unknown location. Several emails were deleted.',
                'category': 'hacking',
                'priority': 'critical',
                'status': 'in_progress',
                'assigned_officer': officer1,
            },
            {
                'complainant': user1,
                'title': 'Online Shopping Fraud',
                'description': 'Unauthorized purchase made on my e-commerce account for $500 worth of electronics.',
                'category': 'online_fraud',
                'priority': 'high',
                'status': 'resolved',
                'assigned_officer': officer1,
            },
            {
                'complainant': user2,
                'title': 'Phishing Email Received',
                'description': 'Received a phishing email impersonating my bank, asking for account details.',
                'category': 'phishing',
                'priority': 'high',
                'status': 'in_progress',
                'assigned_officer': officer2,
            },
            {
                'complainant': user2,
                'title': 'Identity Theft Incident',
                'description': 'Someone opened a credit card in my name without authorization.',
                'category': 'identity_theft',
                'priority': 'critical',
                'status': 'in_progress',
                'assigned_officer': officer1,
            },
            {
                'complainant': user1,
                'title': 'Ransomware Attack',
                'description': 'My personal files were encrypted by ransomware. Attacker demanding payment.',
                'category': 'ransomware',
                'priority': 'critical',
                'status': 'in_progress',
                'assigned_officer': officer2,
            },
            {
                'complainant': user2,
                'title': 'Data Breach - Personal Info Exposed',
                'description': 'My personal data was leaked from a company database.',
                'category': 'data_breach',
                'priority': 'high',
                'status': 'pending',
                'assigned_officer': None,
            },
            {
                'complainant': user1,
                'title': 'Cyberbullying and Harassment',
                'description': 'Receiving threatening messages on social media from unknown users.',
                'category': 'cyberbullying',
                'priority': 'medium',
                'status': 'pending',
                'assigned_officer': None,
            },
            {
                'complainant': user2,
                'title': 'Suspicious Payment Attempts',
                'description': 'Multiple unauthorized payment attempts detected on my PayPal account.',
                'category': 'online_fraud',
                'priority': 'medium',
                'status': 'assigned',
                'assigned_officer': officer1,
            },
            {
                'complainant': user1,
                'title': 'Malware Infection',
                'description': 'Detected malware on my computer - antivirus showing 15 infected files.',
                'category': 'hacking',
                'priority': 'high',
                'status': 'assigned',
                'assigned_officer': officer2,
            },
            {
                'complainant': user2,
                'title': 'Closed Case - Resolved',
                'description': 'Previous case that was successfully investigated and resolved.',
                'category': 'phishing',
                'priority': 'medium',
                'status': 'closed',
                'assigned_officer': officer1,
            },
        ]

        created_count = 0
        for data in complaints_data:
            incident_date = timezone.now() - timedelta(days=7)
            
            complaint, created = Complaint.objects.get_or_create(
                title=data['title'],
                complainant=data['complainant'],
                defaults={
                    'description': data['description'],
                    'category': data['category'],
                    'priority': data['priority'],
                    'status': data['status'],
                    'assigned_officer': data['assigned_officer'],
                    'incident_date': incident_date,
                    'incident_location': 'Online',
                    'affected_system': 'Various',
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample complaints')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total complaints now: {Complaint.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed!')
        )
