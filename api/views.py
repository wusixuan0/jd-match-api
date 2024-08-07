from rest_framework.views import APIView
from rest_framework.response import Response

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, World! - Sixuan"})
    
from rest_framework import generics
from .models import MatchRecord
from .serializers import MatchRecordSerializer

class MatchRecordCreateView(generics.ListCreateAPIView):
    queryset = MatchRecord.objects.all()
    serializer_class = MatchRecordSerializer