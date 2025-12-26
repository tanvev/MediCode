from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from clinics.models import Clinic
from permissions.utils import get_user_role
from visits.models import Visit
from analytics.services import doctor_margin
from analytics.services import total_expenses, net_profit

from .services import (
    clinic_earnings,
    doctor_wise_revenue,
    payment_method_split,
    lab_workload,
    vendor_workload,
    patients_per_day,
    new_vs_repeat,
    busiest_hours,
    busiest_days,
    growth_percentage
)


class OwnerDashboardView(APIView):

    def get(self, request):
        clinic_id = request.query_params.get('clinic')
        if not clinic_id:
            raise PermissionDenied("Clinic required")

        clinic = Clinic.objects.get(id=clinic_id)

        if get_user_role(request.user, clinic) != 'owner':
            raise PermissionDenied("Owner access only")

        data = {
            'total_earnings': clinic_earnings(clinic),
            'doctor_wise_revenue': list(doctor_wise_revenue(clinic)),
            'payment_methods': list(payment_method_split(clinic)),
            'lab_workload': list(lab_workload(clinic)),
            'vendor_workload': list(vendor_workload(clinic)),
        }
        today = date.today()
        last_month_start = today.replace(day=1)
        prev_month_start = (last_month_start - timedelta(days=1)).replace(day=1)
        prev_month_end = last_month_start - timedelta(days=1)

        current_month_visits = Visit.objects.filter(
            clinic=clinic,
            visit_start__date__gte=last_month_start
        ).count()

        prev_month_visits = Visit.objects.filter(
            clinic=clinic,
            visit_start__date__range=[prev_month_start, prev_month_end]
        ).count()

        data.update({
            'patients_per_day': list(patients_per_day(clinic)),
            'new_vs_repeat': new_vs_repeat(clinic),
            'busiest_hours': list(busiest_hours(clinic)),
            'busiest_days': list(busiest_days(clinic)),
            'visit_growth_pct': growth_percentage(
                current_month_visits,
                prev_month_visits),
            'total_expenses': total_expenses(clinic),
            'net_profit': net_profit(clinic),
            'doctor_margins': doctor_margin(clinic),

        })

        return Response(data)
from .services import (
    patients_per_day,
    new_vs_repeat,
    busiest_hours,
    busiest_days,
    growth_percentage
)
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def owner_dashboard_page(request):
    return render(request, 'analytics/owner_dashboard.html')

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from permissions.utils import get_user_role
from .demo_loader import load_demo_data

@login_required
def load_demo(request):
    if not settings.DEMO_MODE:
        return redirect('/login/')

    clinic = load_demo_data(request.user)

    return redirect('/analytics/dashboard/')
