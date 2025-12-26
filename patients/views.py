from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
from django.shortcuts import render, redirect
from .models import Patient
from clinics.models import Clinic


def add_patient(request):
    clinic = Clinic.objects.first()  # temp, will be dynamic later

    if request.method == 'POST':
        Patient.objects.create(
            clinic=clinic,
            patient_id=request.POST.get('patient_id') or None,
            name=request.POST['name'],
            phone=request.POST['phone'],
            medical_alerts=request.POST.get('medical_alerts', ''),
            referred_by=request.POST.get('referred_by', '')
        )
        return redirect('add_patient')

    return render(request, 'patients/add_patient.html')
