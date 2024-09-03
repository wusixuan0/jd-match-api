from django.core.management.base import BaseCommand
from api.email_services.mailchimp_service import schedule_send

class Command(BaseCommand):
    help = 'Performs various MailChimp operations'

    def add_arguments(self, parser):
        parser.add_argument('operation', type=str, help='Specify the operation to perform')
        parser.add_argument('email', type=str, help='Specify the email address to use')

    def handle(self, *args, **options):
        operation = options['operation']
        email = options['email']

        if operation == 'schedule_send':
            response = schedule_send(email, 'daily')
            self.stdout.write(self.style.SUCCESS(f'schedule_send: {response}'))
        else:
            self.stdout.write(self.style.ERROR(f'Invalid operation'))
