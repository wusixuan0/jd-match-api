import os
from pathlib import Path
from django.core.management.base import BaseCommand
from api.models import GeneratedResume
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate HTML resumes and save to database'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='Name of the HTML file in the project root')

    def handle(self, *args, **options):
        file_name = options['file_name']
        file_path = Path(settings.BASE_DIR) / file_name

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            with file_path.open('r', encoding='utf-8') as file:
                html_content = file.read()

            resume_html = GeneratedResume.objects.create(html=html_content)
            self.stdout.write(self.style.SUCCESS(f'Successfully generated and saved resume_html ID: {resume_html.id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

# class Command(BaseCommand):
#     help = 'Generate HTML resumes and save to database'

#     def handle(self, *args, **options):
#         html_content = # import from a file
#         resume_html = GeneratedResume.objects.create(html=html_content)
#         self.stdout.write(self.style.SUCCESS(f'Successfully generated and saved resume_html ID: {resume_html.id}'))


#         # prompt = """
#         # Generate a complete HTML resume with the following requirements:
#         # [Your specific requirements here]
        
#         # The output should be a full HTML document, including <html>, <head>, and <body> tags.
#         # """
