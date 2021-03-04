from django.core.management.base import BaseCommand
import csv
from django.core.mail import EmailMessage

from covid.models import SimulationRun


class Command(BaseCommand):
    help = 'Send a CSV with data on the most recent runs'

    def handle(self, *args, **options):
        sim_list = SimulationRun.objects.all().order_by('-timestamp')[:100]
        rows = []

        for item in sim_list:
            rows.append({
                'state': item.model_input['state'],
                'timestamp': item.timestamp
            })

        with open('/tmp/report.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['state', 'timestamp'])
            writer.writeheader()
            writer.writerows(rows)

        email = EmailMessage(
            subject='SEIRCast Report',
            body="CSV from server",
            to=['snjoroge@nd.edu'],
            reply_to=['snjoroge@nd.edu'],
        )

        with open('/tmp/report.csv') as fp:
            email.attach('report.csv', fp.read(), 'text/csv')

        email.send()
