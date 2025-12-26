from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Payment
from visits.models import Visit
from doctors.models import DoctorProfile


def add_payment(request):
    visits = Visit.objects.all()
    doctors = DoctorProfile.objects.all()

    if request.method == 'POST':
        Payment.objects.create(
            visit_id=request.POST['visit'],
            doctor_id=request.POST.get('doctor') or None,
            billed_amount=request.POST['billed'],
            paid_amount=request.POST['paid'],
            payment_method=request.POST['method'],
            remarks=request.POST.get('remarks', '')
        )
        return redirect('add_payment')

    return render(request, 'payments/add.html', {
        'visits': visits,
        'doctors': doctors
    })

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from .models import Payment
from .serializers import PaymentSerializer
from permissions.utils import get_user_role


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        clinic_id = self.request.query_params.get('clinic')
        role = get_user_role(self.request.user, clinic_id)

        if role != 'owner':
            raise PermissionDenied("Not allowed to access payments")

        return Payment.objects.filter(
            visit__clinic_id=clinic_id
        )
