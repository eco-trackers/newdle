from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profil.models import Profil
from group.models import Group

class Command(BaseCommand):
    help = 'Add admin user to database'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        password = options['password']

        # Create or get the user
        user, created = User.objects.get_or_create(username=username, defaults={'is_staff': True, 'is_superuser': True})
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User '{username}' created and set as admin."))
        else:
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))

        # Create or get the profile
        profile, profile_created = Profil.objects.get_or_create(user=user)
        if profile_created:
            profile.type = 'A'  # Assuming 'A' signifies admin type in your use case
            profile.save()
            self.stdout.write(self.style.SUCCESS(f"Profile for user '{username}' created."))
        else:
            self.stdout.write(self.style.WARNING(f"Profile for user '{username}' already exists."))

        # Optionally, add the user to a group (if any)
        group, _ = Group.objects.get_or_create(name='Default Group')
        profile.group.add(group)
        profile.save()
        self.stdout.write(self.style.SUCCESS(f"User '{username}' added to the default group."))
