from django.core.management.base import BaseCommand
from api.util.opensearch_queries import get_distinct_field

class Command(BaseCommand):
    help = 'Performs various OpenSearch query operations'
    
    def add_arguments(self, parser):
        parser.add_argument('operation', type=str, help='Specify OpenSearch field: searched_job_title, location')
    
    def handle(self, *args, **options):
        operation = options['operation']
        response = get_distinct_field(operation)
        self.stdout.write(self.style.SUCCESS(f'{operation}: {response}'))
