import os
from pathlib import Path
from django.core.management.base import BaseCommand
from api.models import GeneratedResume
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate HTML resumes from files in generated_data folder and save to database'

    def handle(self, *args, **options):
        folder_path = Path(settings.BASE_DIR) / 'generated_data'

        if not folder_path.exists() or not folder_path.is_dir():
            self.stdout.write(self.style.ERROR(f'Folder not found: {folder_path}'))
            return

        html_files = list(folder_path.glob('*.html'))

        if not html_files:
            self.stdout.write(self.style.WARNING('No HTML files found in the generated_data folder.'))
            return

        for file_path in html_files:
            try:
                with file_path.open('r', encoding='utf-8') as file:
                    html_content = file.read()

                resume_html = GeneratedResume.objects.create(html=html_content)
                self.stdout.write(self.style.SUCCESS(f'Successfully generated and saved resume_html ID: {resume_html.id} from file: {file_path.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing file {file_path.name}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Processed {len(html_files)} HTML files from the generated_data folder.'))