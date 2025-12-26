from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, DoctorPayout
from clinics.models import Clinic
from permissions.utils import get_user_role


@login_required
def doctor_payouts(request):
    clinic = Clinic.objects.first()  # dynamic later

    if get_user_role(request.user, clinic) != 'owner':
        return redirect('/login/')

    doctors = DoctorProfile.objects.filter(clinic=clinic)
    payouts = DoctorPayout.objects.filter(clinic=clinic).order_by('-month')

    if request.method == 'POST':
        DoctorPayout.objects.create(
            doctor_id=request.POST['doctor'],
            clinic=clinic,
            month=request.POST['month'],
            amount=request.POST['amount']
        )
        return redirect('doctor-payouts')

    return render(request, 'doctors/payouts.html', {
        'doctors': doctors,
        'payouts': payouts
    })
