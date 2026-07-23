"""
Django management command to mark all existing users as needing password reset.
This ensures compliance with CERT-IN 16-21 character password requirement.
"""
from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Mark all existing users as needing password reset to meet CERT-IN 16-21 character requirement'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm the action without prompting'
        )

    def handle(self, *args, **options):
        # Count existing users who don't need reset
        users_to_update = CustomUser.objects.filter(password_needs_reset=False).count()
        
        if users_to_update == 0:
            self.stdout.write(
                self.style.SUCCESS('All users already marked for password reset.')
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f'This will mark {users_to_update} users as needing password reset.\n'
                'Users will be required to change their password on next login.\n'
            )
        )

        if not options['confirm']:
            confirm = input('Do you want to continue? (yes/no): ').strip().lower()
            if confirm != 'yes':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        # Mark all users as needing password reset
        updated = CustomUser.objects.filter(password_needs_reset=False).update(
            password_needs_reset=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully marked {updated} users for password reset.\n'
                'Users will see a message on next login requiring password update.'
            )
        )
