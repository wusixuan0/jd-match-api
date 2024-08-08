from django.urls import path
from . import views

urlpatterns = [
    path('match/', views.resume_process, name='match-resume'),
]