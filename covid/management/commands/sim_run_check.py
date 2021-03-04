from django.core.management.base import BaseCommand
import csv
from django.core.mail import EmailMessage

from covid.models import SimulationRun

from datetime import datetime


class Command(BaseCommand):
    help = 'Send a CSV with data on the most recent runs'

    def handle(self, *args, **options):
        sim_list = SimulationRun.objects.all().order_by('-timestamp')[:500]
        rows = []
        git_hash = None

        for item in sim_list:
            rows.append({
                'state': item.model_input['state'],
                'counties': ",".join(item.model_input['county']),
                'timestamp': item.timestamp.date()
            })

            if item.model_output and not git_hash:
                if 'git_hash' in item.model_output:
                    git_hash = item.model_output['git_hash']

        start = datetime.now().replace(hour=0, minute=0, second=0)
        end = datetime.now().replace(hour=23, minute=59, second=59)
        jobs_today = SimulationRun.objects.filter(timestamp__range=[start, end]).count()

        body = "Jobs today: {}\nLatest Git Hash: {}".format(jobs_today, git_hash)

        with open('/tmp/report.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['state', 'counties', 'timestamp'])
            writer.writeheader()
            writer.writerows(rows)

        email = EmailMessage(
            subject='SEIRCast Report',
            body=body,
            to=['snjoroge@nd.edu'],
            reply_to=['snjoroge@nd.edu'],
        )

        with open('/tmp/report.csv') as fp:
            email.attach('report.csv', fp.read(), 'text/csv')

        email.send()