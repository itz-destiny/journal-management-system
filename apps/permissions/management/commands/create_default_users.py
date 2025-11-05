from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.permissions.models import CustomUser
from apps.reviewer.models import Reviewer
from apps.user.models import NormalUser


class Command(BaseCommand):
    help = 'Create default admin and reviewer accounts'

    def handle(self, *args, **kwargs):
        # Create groups first
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        reviewer_group, _ = Group.objects.get_or_create(name='Reviewer')
        user_group, _ = Group.objects.get_or_create(name='User')

        # Create Admin User
        admin_username = 'admin'
        admin_password = 'Admin@2025'
        admin_email = 'admin@uniquejms.com'
        
        if not CustomUser.objects.filter(username=admin_username).exists():
            admin_user = CustomUser.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                user_type=admin_group
            )
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'✅ Admin created: {admin_username} / {admin_password}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Admin user already exists'))

        # Create Reviewer User
        reviewer_username = 'reviewer'
        reviewer_password = 'Reviewer@2025'
        reviewer_email = 'reviewer@uniquejms.com'
        
        if not CustomUser.objects.filter(username=reviewer_username).exists():
            reviewer_user = CustomUser.objects.create_user(
                username=reviewer_username,
                email=reviewer_email,
                password=reviewer_password,
                user_type=reviewer_group
            )
            reviewer_user.groups.add(reviewer_group)
            
            # The Reviewer profile is automatically created by the post_save signal
            # Just update the profile fields
            try:
                reviewer_profile = reviewer_user.reviewer
                reviewer_profile.full_name = 'Default Reviewer'
                reviewer_profile.email = reviewer_email
                reviewer_profile.save()
            except Reviewer.DoesNotExist:
                # If signal didn't fire, create manually
                Reviewer.objects.create(
                    reviewer_user=reviewer_user,
                    full_name='Default Reviewer',
                    email=reviewer_email,
                    contact='N/A',
                    address='N/A'
                )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Reviewer created: {reviewer_username} / {reviewer_password}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Reviewer user already exists'))

        # Print credentials summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('DEFAULT ACCOUNTS CREATED'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS(f'\n🔐 ADMIN LOGIN:'))
        self.stdout.write(self.style.SUCCESS(f'   Username: {admin_username}'))
        self.stdout.write(self.style.SUCCESS(f'   Password: {admin_password}'))
        self.stdout.write(self.style.SUCCESS(f'\n🔐 REVIEWER LOGIN:'))
        self.stdout.write(self.style.SUCCESS(f'   Username: {reviewer_username}'))
        self.stdout.write(self.style.SUCCESS(f'   Password: {reviewer_password}'))
        self.stdout.write(self.style.SUCCESS('\n' + '='*50 + '\n'))
