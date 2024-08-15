from django.urls import path
from . import views

urlpatterns = [
    path('match/', views.resume_process, name='match-resume'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('feedback/', views.feedback, name='feedback'),
]