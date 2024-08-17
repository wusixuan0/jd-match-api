import os
import time
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from supabase import create_client
from django_ratelimit.decorators import ratelimit
from api.services import resume_service
from api.util.send_log import send_log
from .models import TemporaryTransaction, UserEmail, Resume, JobRecommendation, UserFeedback
from api.email_services.mailchimp_service import subscribe_user_to_list
from django.db import IntegrityError

TEST = 'RENDER' not in os.environ

@ratelimit(key='ip', rate='5/m', block=False)
@api_view(['POST'])
def resume_process(request):
    start_time = time.time()
    start_time_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    send_log(f">>>Django API Receive Request at {start_time_datetime}")

    if getattr(request, 'limited', False):
        return Response({"error": "You have exceeded the request limit (5 requests per minute). Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    version = request.data.get('version') or 'version1'
    model_name = request.data.get('model_name') or 'gemini-1.5-flash'
    file_obj = request.data.get('file')
    
    if not file_obj:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not TEST:
        send_log("Uploading Resume PDF File to S3 bucket.")
        upload_result = upload(file_obj)
    else:
        upload_result = os.environ.get("RESUME_URL_EXAMPLE")    
  
    if isinstance(upload_result, str):              
        match_result = resume_service(upload_result, version, model_name, is_url=True, top_n=5)
        temp_transaction = TemporaryTransaction.objects.create(
            file_url=upload_result,
            file_summary=match_result.get("resume_summary"),
            ranked_ids= match_result.get("ranked_ids"),
        )
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        end_time_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        send_log(f"<<<Django API Request Finished at {end_time_datetime}. Duration: {duration} seconds")
        
        return Response({
            "ranked_jds": match_result.get("ranked_docs"),
            "transaction_id": temp_transaction.id,
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": str(upload_result)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def feedback(request):
    user_email_id = request.data.get('email_id')
    if user_email_id:
        user_email = UserEmail.objects.get(id=user_email_id)
        UserFeedback.objects.create(user_email=user_email,applied_job_ids=request.data.get('applied'),user_ranking=request.data.get('rankings'),)
    else:
        temp_transaction = TemporaryTransaction.objects.get(id=request.data.get('transaction_id'))
        UserFeedback.objects.create(temporary_transaction=temp_transaction,applied_job_ids=request.data.get('applied'),user_ranking=request.data.get('rankings'),)
    return Response({"message": "Feedback successful"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def subscribe(request):
    try:
        with transaction.atomic():
            transaction_id = request.data.get('transaction_id')
            email = request.data.get('email')
            frequency = request.data.get('frequency')

            if not all([transaction_id, email, frequency]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                temp_transaction = TemporaryTransaction.objects.get(id=transaction_id)
            except ObjectDoesNotExist:
                return Response({"error": "Invalid transaction ID"}, status=status.HTTP_404_NOT_FOUND)
            try:
                user_email = UserEmail.objects.create(email=email, frequency=frequency.lower())
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    # Handle the duplicate key error
                    return Response({'error': 'Email address already exists'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Handle other IntegrityError cases
                    return Response({'error': 'An error occurred while creating the user email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            resume = Resume.objects.create(
                user_email=user_email,
                resume_url=temp_transaction.file_url,
                resume_summary=temp_transaction.file_summary
            )
            JobRecommendation.objects.create(
                user_email=user_email,
                resume=resume,
                ranked_job_ids=temp_transaction.ranked_ids,
            )
            convert_feedback_to_permanent(temp_transaction, user_email)
            # temp_transaction.delete()
            try:
                subscribe_user_to_list(email)
            except Exception as e:
                return Response({'error': {e.text}}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Subscription successful","email_id": user_email.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def convert_feedback_to_permanent(temp_transaction, user_email):
    UserFeedback.objects.filter(temporary_transaction=temp_transaction).update(
        user_email=user_email,
        temporary_transaction=None
    )
 
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