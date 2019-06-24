from django.core.management.base import BaseCommand, CommandError

import environ
env = environ.Env()

from users.models import User

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        email=env('ADMIN_EMAIL', default=None)

        if email:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    is_staff=True,
                    is_superuser=True,
                    username=env('ADMIN_USERNAME', default='admin'),
                    email=email,
                    password=env('ADMIN_PASSWORD')
                )
                self.stdout.write(self.style.SUCCESS('DCC: Admin user created!'))
            elif bool(env('ADMIN_RESET', default=False)):
                user = User.objects.get(email=email)
                user.set_password(env('ADMIN_PASSWORD'))
                user.save()
                self.stdout.write(self.style.SUCCESS('DCC: Admin password reset!'))
            else:
                self.stdout.write(self.style.SUCCESS('DCC: Admin user already exists!'))
        else:
            self.stdout.write(self.style.WARNING('DCC: Did not create admin user!'))