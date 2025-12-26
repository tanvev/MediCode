from django.urls import path
from .views import add_patient

urlpatterns = [
    path('add/', add_patient, name='add_patient'),
]
