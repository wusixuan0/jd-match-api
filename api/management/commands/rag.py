from django.core.management.base import BaseCommand
from api.util.rag.rag import load_pdf, format_docs, summrize_prompt, question_analysis_prompt, rag
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('operation', type=str, help='Specify the operation to perform')
    
    def handle(self, *args, **options):
        operation = options['operation']

        if operation == 'load_pdf':
            file_path = Path(settings.BASE_DIR) / 'generated_data' / 'book.pdf'

            docs = load_pdf(file_path)
            # docs = docs[34:51]
            docs_3 = docs[52:68]
            chapters = [docs_3]
            summrize_prompt="""Please provide a detailed explanation of the following chapter from the book "In Search of Schrodinger's Cat: Quantum Physics And Reality" by John Gribbin.
* Strictly adhere to the author's thought process and explanations.
* Use extremely simple terms and language.
* Explain experiments and events in details, include what experiment is, the process and significance. 
* Include questions and answers that a beginner might ask.
* Aim for an explanation that's 5000 words long, to ensure thorough coverage of the material.
"""
            for index, chapter_docs in enumerate(chapters):
                chap_text = format_docs(chapter_docs)
                with open(f'{index}.txt', 'w') as file:
                    file.write(summrize_prompt)
                    file.write(chap_text)
        
        # elif operation == 'rag':
        #     response = rag(question)
        #     self.stdout.write(self.style.SUCCESS(f'rag: {response}'))
        else:
            self.stdout.write(self.style.ERROR(f'Invalid operation'))