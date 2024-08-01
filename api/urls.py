from .views import HelloWorld
from django.urls import path, include

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
]