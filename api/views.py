from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from supabase import create_client
from api.services import resume_service
import time

@api_view(['POST'])
def resume_process(request):
    file_obj = request.data.get('file')
    if not file_obj:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    upload_result = upload(file_obj)

    if isinstance(upload_result, str):
        result = resume_service(upload_result)
        return Response({"ranked_jds": result}, status=status.HTTP_200_OK)
    else:
        return Response({"error": str(upload_result)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def upload(file_obj):
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
    if not (SUPABASE_URL and SUPABASE_ANON_KEY):
        raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY environment variables are not set")

    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    bucket_name = os.environ.get('BUCKET_NAME')
    folder_name = os.environ.get('FOLDER_NAME')

    file_content = file_obj.read() # Convert InMemoryUploadedFile to bytes
    file_name = f"{int(time.time())}_{file_obj.name}"
    
    try:
        response = supabase.storage.from_(bucket_name).upload(f'{folder_name}/{file_name}', file_content)

        file_key = response.json().get('Key')
        
        S3_URL = os.environ.get('S3_URL')
        file_url=f"{S3_URL}{file_key}"
        print(f'File uploaded with url: {file_key}')
        return file_url
    except Exception as e:
        return e