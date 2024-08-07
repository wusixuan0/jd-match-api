from django.urls import path, include
from .views import HelloWorld, MatchRecordCreateView

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('match_records/', MatchRecordCreateView.as_view(), name='match-record-list-create'),
]