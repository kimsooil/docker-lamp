from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model 
from django.core.mail import EmailMessage
from .email_helpers import generate_email_body


User = get_user_model()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--emails', nargs='*', type=str)
        parser.add_argument('--force', action='store_true', help='Forces sending of emails even if one has already been sent.',)

    def handle(self, *args, **options):
        if options['emails']:
            users = User.objects.filter(email__in=options['emails'])
            if not options['force']:
                users = users.filter(onboarding_email_sent=False)
        else:
            users = User.objects.filter(onboarding_email_sent=False).exclude(email=None) # , username__contains="@"
        for user in users:
            self.stdout.write('Processing user {}'.format(user))
            username = user.username
            password = User.objects.make_random_password()
            try:
                email = EmailMessage(
                    subject='Welcome to SEIRcast - Account Information',
                    body=generate_email_body(username, password),
                    to=[user.email],
                    cc=['Edwin Michael <emichael@nd.edu>'],
                    reply_to=['Edwin Michael <emichael@nd.edu>'],
                )
                email.send(fail_silently=False)
                user.onboarding_email_sent = True
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS('Email sent sucessfully to {}'.format(user.email)))
            except:
                self.stdout.write(self.style.ERROR('Error sending email to {}'.format(user.email)))

        self.stdout.write(self.style.SUCCESS('Successfully sent onboarding emails'))