import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from profil.models import Profil
from group.models import Group

class Command(BaseCommand):
    help = 'Load users from a CSV file and create default users in the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be processed')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"The file {csv_file_path} does not exist."))
            return

        User = get_user_model()
        data = []

        with open(csv_file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                data.append({
                    "nom": row.get("NOM", "").strip().lower(),
                    "prenom": row.get("Prénom", "").strip().lower(),
                    "email": row.get("email", "").strip().lower(),
                    "password": row.get("password", "").strip(),
                    "role": row.get("role", "").strip().lower(),
                })

        for entry in data:
            first_name = entry["prenom"]
            last_name = entry["nom"]
            email = entry["email"]
            role = entry["role"]
            default_password = entry["password"] or User.objects.make_random_password()

            if first_name and last_name:
                username = f"{first_name}.{last_name}@uha.fr"

                if role == 'student':
                    user_type = '0'
                elif role == 'professor':
                    user_type = '1'
                elif role == 'admin':
                    user_type = '2'
                else:
                    user_type = '0'

                user, created = User.objects.get_or_create(username=username, defaults={'first_name': first_name, 'last_name': last_name})

                if created:
                    user.set_password(default_password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"User '{username}' created."))
                else:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.set_password(default_password)
                    user.save()
                    self.stdout.write(self.style.WARNING(f"User '{username}' updated."))

                profile, profile_created = Profil.objects.update_or_create(
                    user=user,
                    defaults={'type': user_type}
                )

                default_group, group_created = Group.objects.get_or_create(name='Default Group')
                profile.group.add(default_group)

        self.stdout.write(self.style.SUCCESS("Users and profiles created or updated successfully."))
