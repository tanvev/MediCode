from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Vendor, VendorAssignment
from visits.models import Visit
from doctors.models import DoctorProfile
from django.contrib.auth.decorators import login_required


@login_required
def assign_vendor(request, visit_id):
    doctor = DoctorProfile.objects.get(user=request.user)
    visit = Visit.objects.get(id=visit_id, doctor=doctor)

    vendors = Vendor.objects.filter(clinic=visit.clinic, is_active=True)

    if request.method == 'POST':
        VendorAssignment.objects.create(
            visit=visit,
            vendor_id=request.POST['vendor'],
            purpose=request.POST['purpose']
        )
        return redirect('doctor_visits')

    return render(request, 'doctors/assign_vendor.html', {
        'visit': visit,
        'vendors': vendors
    })
