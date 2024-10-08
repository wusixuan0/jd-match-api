import time
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django_ratelimit.decorators import ratelimit
from api.services import resume_service, employer_service
from api.util.send_log import send_log
from .models import TemporaryTransaction, UserEmail, Resume, JobRecommendation, UserFeedback
from api.email_services.mailchimp_service import subscribe_user_to_list, send_one
from api.util.es_query_jd_id import opensearch_get_jd_by_id
from django.db import IntegrityError
import json

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
    file_category = request.data.get('file_category')

    if not file_obj:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if file_category == 'resume':
            match_result = resume_service(file_obj, version, model_name, is_url=True, top_n=5)
            temp_transaction = TemporaryTransaction.objects.create(
                file_summary=match_result.get("resume_summary"),
                ranked_ids= json.dumps(match_result.get("ranked_ids")),
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
            match_result = employer_service(file_obj, version, model_name, top_n=5)
            return Response({
                "match_result": match_result,
            }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    email = request.data.get('email')
    frequency = request.data.get('frequency')
    transaction_id = request.data.get('transaction_id')
    
    if not all([transaction_id, email, frequency]):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        subscribe_user_to_list(email)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            try:
                temp_transaction = TemporaryTransaction.objects.get(id=transaction_id)
            except ObjectDoesNotExist:
                return Response({"error": "Invalid transaction ID"}, status=status.HTTP_404_NOT_FOUND)

            try:
                user_email = UserEmail.objects.get(email=email)
            except ObjectDoesNotExist:
                try:
                    user_email = UserEmail.objects.create(email=email, frequency=frequency.lower())
                except IntegrityError as e:
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
            ranked_ids= json.loads(temp_transaction.ranked_ids)
            ranked_docs = opensearch_get_jd_by_id(ranked_ids)
            job_matched_time = temp_transaction.created_at
            send_one(email, ranked_docs, job_matched_time)
            # temp_transaction.delete()
        
        return Response({"message": "Subscription successful","email_id": user_email.id}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def convert_feedback_to_permanent(temp_transaction, user_email):
    UserFeedback.objects.filter(temporary_transaction=temp_transaction).update(
        user_email=user_email,
        temporary_transaction=None
    )