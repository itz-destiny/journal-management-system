from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create default groups for the Journal Management System'

    def handle(self, *args, **kwargs):
        # Create User/Author group
        user_group, created = Group.objects.get_or_create(name='User')
        if created:
            self.stdout.write(self.style.SUCCESS('Created User group'))
        else:
            self.stdout.write(self.style.WARNING('User group already exists'))

        # Create Reviewer group
        reviewer_group, created = Group.objects.get_or_create(name='Reviewer')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Reviewer group'))
        else:
            self.stdout.write(self.style.WARNING('Reviewer group already exists'))

        # Create Editor group
        editor_group, created = Group.objects.get_or_create(name='Editor')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Editor group'))
        else:
            self.stdout.write(self.style.WARNING('Editor group already exists'))

        # Create Admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admin group'))
        else:
            self.stdout.write(self.style.WARNING('Admin group already exists'))

        self.stdout.write(self.style.SUCCESS('All groups are ready!'))
