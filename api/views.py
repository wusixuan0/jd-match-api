
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework import generics
from .models import MatchRecord
from .serializers import MatchRecordSerializer
from api.services import resume_service

class ResumeProcessView(APIView):
    def post(self, request):
        url = request.data.get('url')

        result = resume_service(url)
        return Response(result, status=status.HTTP_200_OK)

class HelloWorld(APIView):
    def get(self, request):
        resume_url="https://daaouztnkoascsishisv.supabase.co/storage/v1/object/public/icons/resumes/test_resume.pdf?t=2024-08-07T18%3A54%3A47.255Z"
        return Response({"ranked_jds": resume_service(resume_url)})
    
class MatchRecordCreateView(generics.ListCreateAPIView):
    queryset = MatchRecord.objects.all()
    serializer_class = MatchRecordSerializer