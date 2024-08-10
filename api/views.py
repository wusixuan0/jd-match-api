import os
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from supabase import create_client
from django_ratelimit.decorators import ratelimit
from api.services import resume_service
from api.util.send_log import send_log

# TEST = 'RENDER' not in os.environ

@ratelimit(key='ip', rate='5/m', block=False)
@api_view(['POST'])
def resume_process(request):
    send_log(">>>Uploading Resume PDF File to S3 bucket.")
    if getattr(request, 'limited', False):
        return Response(
            {"error": "You have exceeded the request limit (5 requests per minute). Please try again later."},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    
    version = request.data.get('version') or 'version1'

    # if TEST:
    #     result = resume_service(os.environ.get("RESUME_URL_EXAMPLE"), version, model_name='gemini-1.5-pro', top_n=5)
    #     return Response({"ranked_jds": result}, status=status.HTTP_200_OK)
    
    file_obj = request.data.get('file')
    
    if not file_obj: # TODO test exception, refactor
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    upload_result = upload(file_obj)

    if isinstance(upload_result, str):
        result = resume_service(upload_result, version, model_name='gemini-1.5-flash', top_n=5)
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
        send_log(f'<<<File Uploaded with file key: {file_name}')
        return file_url
    except Exception as e:
        return e