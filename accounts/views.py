from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from clinics.models import ClinicMembership

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            email=request.POST['email'],
            password=request.POST['password']
        )

        if user:
            login(request, user)

            membership = ClinicMembership.objects.filter(
                user=user,
                is_active=True
            ).first()

            if not membership:
                return render(request, 'auth/login.html', {
                    'error': 'No clinic access'
                })

            if membership.role == 'owner':
                return redirect('/analytics/dashboard/')
            elif membership.role == 'associate':
                return redirect('/doctor/visits/')
            else:
                return redirect('/patients/add/')

        return render(request, 'auth/login.html', {
            'error': 'Invalid credentials'
        })

    return render(request, 'auth/login.html')
