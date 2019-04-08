print("---------------------------------------------Start Create Admin User")

import environ
env = environ.Env()

import django
django.setup()

from users.models import User

email=env('ADMIN_EMAIL', default=None)

if email:
    print (email)
    if not User.objects.filter(email=email).exists():
        print ("Admin user doesn't exist.")
        user = User.objects.create_user(
            is_staff=True,
            is_superuser=True,
            username=env('ADMIN_USERNAME', default='admin'),
            email=email,
            password=env('ADMIN_PASSWORD')
        )
        print ("Created admin user: ", user.email)
    elif bool(env('ADMIN_RESET', default=False)):
        print("Reset password....")
        user = User.objects.get(email=email)
        user.set_password(env('ADMIN_PASSWORD'))
        user.save()

print("---------------------------------------------End Create Admin User")