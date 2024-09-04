from django.core.management.base import BaseCommand
from api.email_services.mailchimp_service import schedule_send, send_one, subscribe_user_to_list

class Command(BaseCommand):
    help = 'Performs various MailChimp operations'

    def add_arguments(self, parser):
        parser.add_argument('operation', type=str, help='Specify the operation to perform')
        # parser.add_argument('email', type=str, help='Specify the email address to use')
        parser.add_argument('frequency', type=str, help='Specify the frequency to use')

    def handle(self, *args, **options):
        operation = options['operation']
        # email = options['email']
        arg = options['frequency']

        if operation == 'schedule_send':
            response = schedule_send(arg)
            self.stdout.write(self.style.SUCCESS(f'schedule_send: {response}'))
        # elif operation == 'send_one':
        #     ranked_ids=["YS8jTZEBIvxPMcUySMeb", "Gi9JUpEBIvxPMcUyA8jQ", "_i9iM5EBIvxPMcUyymMPQ", "hi-EOJEBIvxPMcUyXMRA", "yC_7R5EBIvxPMcUyz8ah"]
        #     from api.util.opensearch_queries import opensearch_get_jd_by_id
        #     ranked_docs=opensearch_get_jd_by_id(ranked_ids)
        #     from datetime import datetime
        #     job_matched_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
            
        #     import os;email = os.environ.get('DEFAULT_FROM_EMAIL')
        #     response = send_one(email, ranked_docs, job_matched_time)
        #     self.stdout.write(self.style.SUCCESS(f'send_one: {response}'))
        elif operation == 'unsubscribe':
            response = subscribe_user_to_list(arg)

        else:
            self.stdout.write(self.style.ERROR(f'Invalid operation'))
