from django.core.management.base import BaseCommand
from api.email_services.mailchimp_service import generate_confirm_email_content, send_all_working
import os

class Command(BaseCommand):
    help = 'Performs various MailChimp operations'

    def add_arguments(self, parser):
        parser.add_argument('operation', type=str, help='Specify the operation to perform: send_test, generate_email_content')
        parser.add_argument('email', type=str, help='Specify the email address to use')

    def handle(self, *args, **options):
        operation = options['operation']
        email = options['email']

        if operation == 'send_test':
            response = send_all_working(email)
            self.stdout.write(self.style.SUCCESS(f'All sent: {response}'))
        elif operation == 'generate_email_content':
            response = generate_confirm_email_content(email)
            self.stdout.write(self.style.SUCCESS(f'Email content generated: {response}'))
        else:
            self.stdout.write(self.style.ERROR(f'Invalid operation: use "send_test" or "generate_email_content"'))
