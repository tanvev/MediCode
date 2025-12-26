from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Visit
from .serializers import VisitSerializer


class VisitViewSet(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

from django.shortcuts import render, redirect
from .models import Visit
from clinics.models import Clinic
from patients.models import Patient
from doctors.models import DoctorProfile


def create_visit(request):
    clinic = Clinic.objects.first()
    patients = Patient.objects.filter(clinic=clinic)
    doctors = DoctorProfile.objects.filter(clinic=clinic)

    if request.method == 'POST':
        Visit.objects.create(
            clinic=clinic,
            patient_id=request.POST['patient'],
            doctor_id=request.POST['doctor'],
            notes=request.POST.get('notes', '')
        )
        return redirect('create_visit')

    return render(request, 'visits/create.html', {
        'patients': patients,
        'doctors': doctors
    })
from django.contrib.auth.decorators import login_required
from doctors.models import DoctorProfile


@login_required
def doctor_visits(request):
    doctor = DoctorProfile.objects.get(user=request.user)
    visits = Visit.objects.filter(doctor=doctor).order_by('-visit_start')

    return render(request, 'doctors/visits.html', {
        'visits': visits
    })

@login_required
def edit_visit(request, visit_id):
    doctor = DoctorProfile.objects.get(user=request.user)
    visit = Visit.objects.get(id=visit_id, doctor=doctor)

    if request.method == 'POST':
        visit.notes = request.POST.get('notes', '')
        visit.save()
        return redirect('doctor_visits')

    return render(request, 'doctors/edit_visit.html', {
        'visit': visit
    })
