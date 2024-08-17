from django.core.management.base import BaseCommand
from api.email_services.mailchimp_service import generate_email_content, send_all_subscriber, send_single_client, subscribe_user_to_list
import os

class Command(BaseCommand):
    help = 'Performs various MailChimp operations'

    def add_arguments(self, parser):
        parser.add_argument('operation', type=str, help='Specify the operation to perform: job_recommendation, subscribe_user, generate_campaign')

    def handle(self, *args, **options):
        operation = options['operation']

        if operation == 'send_all':
            response = send_all_subscriber('daily')
            self.stdout.write(self.style.SUCCESS(f'All sent: {response}'))
        
        elif operation == 'send_one':
            response = send_single_client(os.environ.get('DEFAULT_FROM_EMAIL'))
            self.stdout.write(self.style.SUCCESS(f'sent: {response}'))
        
        elif operation == 'generate_email_content':
            response = generate_email_content(os.environ.get('DEFAULT_FROM_EMAIL'))
            self.stdout.write(self.style.SUCCESS(f'Email content generated: {response}'))
        
        else:
            self.stdout.write(self.style.ERROR(f'Invalid operation: {operation}'))