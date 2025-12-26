from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Lab, LabAssignment
from visits.models import Visit
from doctors.models import DoctorProfile
from django.contrib.auth.decorators import login_required


@login_required
def assign_lab(request, visit_id):
    doctor = DoctorProfile.objects.get(user=request.user)
    visit = Visit.objects.get(id=visit_id, doctor=doctor)

    labs = Lab.objects.filter(clinic=visit.clinic, is_active=True)

    if request.method == 'POST':
        LabAssignment.objects.create(
            visit=visit,
            lab_id=request.POST['lab'],
            work_description=request.POST['work']
        )
        return redirect('doctor_visits')

    return render(request, 'doctors/assign_lab.html', {
        'visit': visit,
        'labs': labs
    })
