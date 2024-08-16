from django.core.management.base import BaseCommand
from api.email_services.mailchimp_service import send_job_recommendation

class Command(BaseCommand):
    help = 'Generates content using the MailChimp service'

    def handle(self, *args, **options):
        response = send_job_recommendation()
        self.stdout.write(self.style.SUCCESS(f'Email sent: {response}'))