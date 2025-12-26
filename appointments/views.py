from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

from django.shortcuts import render, redirect
from .models import Appointment
from clinics.models import Clinic
from patients.models import Patient


def book_appointment(request):
    clinic = Clinic.objects.first()
    patients = Patient.objects.filter(clinic=clinic)

    if request.method == 'POST':
        Appointment.objects.create(
            clinic=clinic,
            patient_id=request.POST['patient'],
            appointment_time=request.POST.get('appointment_time') or None,
            is_walk_in=bool(request.POST.get('is_walk_in'))
        )
        return redirect('book_appointment')

    return render(request, 'appointments/book.html', {'patients': patients})
